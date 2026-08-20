# Library Data Cleaner

## What this is

The library was checking the quality of their data by hand. It took too long and things got
missed, because people get bored and make mistakes when they are reading through thousands of
rows. This is a small Python app that does the same job automatically, the same way, every time
it runs.

It takes the two raw CSV exports from the library system, cleans them, writes out clean copies,
and records what it did in a metrics file so there is a record of every run.

## What it does

It takes the two raw CSV exports from the library system, cleans them, writes out clean copies,
and records what it did in a metrics file so there is a record of every run.
There are two datasets and one python function for each.

**Customers** (`03_Library SystemCustomers.csv`)

1. Loads the file.
2. Drops duplicate rows and counts how many it dropped.
3. Drops any row with a missing value and counts those too.
4. Resets the index and writes `CleanedCustomers.csv`.

**Books** (`03_Library Systembook.csv`)

1. Loads the file.
2. Drops duplicates and rows with missing values, same as above.
3. Strips the stray `"` characters out of the `Book checkout` column.
4. Tidies the column headers, so `Book checkout` becomes `book_checkout`. Everything goes
   lowercase, and spaces, dashes and punctuation all become underscores. That way the rest of the
   code does not have to care how the export was formatted.
5. Works out how long each book was out, using `days_between()`. It parses `book_checkout` and
   `book_returned` as UK dates (day first), takes the difference in whole days, and puts it in a
   new `days_borrowed` column.
6. Writes `CleanedBooks.csv`.


### Bad dates

Dates that cannot be parsed are not allowed to stop the run. `pd.to_datetime` is called with
`errors="coerce"`, so anything unreadable becomes `NaT` and `days_borrowed` is left blank for that
row. The function counts how many values failed and hands that number back, so the failures get
reported instead of quietly disappearing.

## The metrics file

Every run appends one row per dataset to `cleaning_metrics.csv`. The header is only written the
first time, so the file builds up a history rather than being overwritten.

Each row holds:

 Column - What it is 
 
 run_id - A UUID generated once per run, shared by both datasets, so the two rows can be tied together 
 stage - Always clean at the moment. Room for more stages later 
 dataset - customers or books 
 status - completed or failed 
 started_at, ended_at, duration_seconds - How long that dataset took 
 rows_in, rows_out - Row counts before and after 
 duplicates_removed, null_rows_dropped, date_parse_failures - What was actually cleaned out 
 output_file - The clean file that was written 
 error - The error type and message if it failed, otherwise blank 

This is the part that replaces the manual quality check. Instead of someone eyeballing the data,
you can look at the numbers and see straight away if a run pulled in fewer rows than usual, or
dropped far more rows than normal, or hit a pile of unreadable dates.

## Error handling

Each dataset is wrapped in its own `try`/`except`. If customers fails, books still runs. A failure
still gets a metrics row written, with the status set to `failed` and the error message recorded,
so a broken run leaves a trace instead of nothing at all. Any columns that were not filled in are
written as blanks.

## Built to run on its own

The app is written to be run automatically rather than by a person sitting at a keyboard, which is
why the metrics are structured the way they are.

- It takes no arguments and needs no input while it runs, so it can be run unattended.

- Every run is tagged with a `run_id`, and the metrics are appended rather than overwritten, so you
  build up a run by run history of data quality.
- The cleaned CSVs are just files in the same folder, so anything downstream can pick them up.

The library gets clean data and a quality report without anyone having to touch it.
