import csv
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent

INPUTCustomers = DATA / "03_Library SystemCustomers.csv"
OUTPUTCustomers = DATA / "CleanedCustomers.csv"

INPUTBooks = DATA / "03_Library Systembook.csv"
OUTPUTBooks = DATA / "CleanedBooks.csv"

METRICS = DATA / "cleaning_metrics.csv"

METRIC_FIELDS = [
    "run_id", "stage", "dataset", "status",
    "started_at", "ended_at", "duration_seconds",
    "rows_in", "duplicates_removed", "null_rows_dropped",
    "date_parse_failures", "rows_out",
    "output_file", "error",
]

RUN_ID = str(uuid.uuid4())


def now():
    return datetime.now()


def write_metrics(row):
    """Append one row per dataset per run. Header is written only on first use."""
    new_file = not METRICS.exists()
    with open(METRICS, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=METRIC_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow({key: row.get(key, "") for key in METRIC_FIELDS})


def days_between(df, start_col, end_col, new_col="days_between"):
    """Add a column holding the whole-day difference between two date columns.

    Also returns the number of values that failed to parse (NaT), so the
    caller can report on them.
    """
    start = pd.to_datetime(df[start_col], dayfirst=True, errors="coerce")
    end   = pd.to_datetime(df[end_col],   dayfirst=True, errors="coerce")

    parse_failures = int(start.isna().sum() + end.isna().sum())

    df = df.copy()
    df[new_col] = (end - start).dt.days
    return df, parse_failures


def CleanCustomers():
    Customers = pd.read_csv(INPUTCustomers)
    rows_in = len(Customers)
    print(f"Loaded {rows_in:,} rows from {INPUTCustomers.name}")

    #Remove Duplicates
    dupes = int(Customers.duplicated().sum())
    Customers = Customers.drop_duplicates()
    print(f"Removed {dupes:,} duplicate rows")

    #Remove Rows with missing values
    nulls = int(Customers.isna().any(axis=1).sum())
    Customers = Customers.dropna()
    print(f"Removed {nulls:,} rows with missing values")

    Customers = Customers.reset_index(drop=True)
    Customers.to_csv(OUTPUTCustomers, index=False, encoding="utf-8-sig")
    print(f"wrote {len(Customers):,} clean rows to {OUTPUTCustomers}")
    print(Customers)

    return {
        "dataset": "customers",
        "rows_in": rows_in,
        "duplicates_removed": dupes,
        "null_rows_dropped": nulls,
        "date_parse_failures": 0,          # no date columns in this file
        "rows_out": len(Customers),
        "output_file": OUTPUTCustomers.name,
    }


def CleanBooks():
    Books = pd.read_csv(INPUTBooks)
    rows_in = len(Books)
    print(f"Loaded {rows_in:,} rows from {INPUTBooks.name}")

    #Remove Duplicates
    dupes = int(Books.duplicated().sum())
    Books = Books.drop_duplicates()
    print(f"Removed {dupes:,} duplicate rows")

    #Remove Rows with missing values
    nulls = int(Books.isna().any(axis=1).sum())
    Books = Books.dropna()
    print(f"Removed {nulls:,} rows with missing values")

    #Sort out the dates
    Books['Book checkout'] = Books['Book checkout'].str.replace('"', '', regex=False)

    #Sort Column Headers
    Books.columns = (
    Books.columns
      .str.strip()
      .str.lower()
      .str.replace(r"[^\w]+", "_", regex=True)   # spaces, dashes, punctuation → _
      .str.strip("_")
)

    Books, parse_failures = days_between(Books, "book_checkout", "book_returned", "days_borrowed")
    print(f"{parse_failures:,} date values failed to parse")

    Books = Books.reset_index(drop=True)
    Books.to_csv(OUTPUTBooks, index=False, encoding="utf-8-sig")
    print(f"wrote {len(Books):,} clean rows to {OUTPUTBooks}")
    print(Books)

    return {
        "dataset": "books",
        "rows_in": rows_in,
        "duplicates_removed": dupes,
        "null_rows_dropped": nulls,
        "date_parse_failures": parse_failures,
        "rows_out": len(Books),
        "output_file": OUTPUTBooks.name,
    }


if __name__ == "__main__":
    for name, clean in (("customers", CleanCustomers), ("books", CleanBooks)):
        started = now()
        try:
            metrics = clean()
            metrics["status"] = "completed"
            metrics["error"] = ""
        except Exception as exc:
            metrics = {"dataset": name, "status": "failed",
                       "error": f"{type(exc).__name__}: {exc}"}
            print(f"{name} FAILED: {metrics['error']}")

        ended = now()
        metrics["run_id"] = RUN_ID
        metrics["stage"] = "clean"
        metrics["started_at"] = started.isoformat(timespec="seconds")
        metrics["ended_at"] = ended.isoformat(timespec="seconds")
        metrics["duration_seconds"] = round((ended - started).total_seconds(), 3)
        write_metrics(metrics)

    print(f"metrics appended to {METRICS} (run_id {RUN_ID})")