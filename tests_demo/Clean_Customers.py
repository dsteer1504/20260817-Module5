import pandas as pd
from pathlib import Path

DATA = Path("/data/cleaning_data_task")
OUT = Path("/out")

INPUTCustomers = DATA / "03_Library SystemCustomers.csv"
OUTPUTCustomers = OUT / "CleanedCustomers.csv"

INPUTBooks = DATA / "03_Library Systembook.csv"
OUTPUTBooks = OUT / "CleanedBooks.csv"


def days_between(df, start_col, end_col, new_col="days_between"):
    """Add a column holding the whole-day difference between two date columns."""
    start = pd.to_datetime(df[start_col], dayfirst=True, errors="coerce")
    end   = pd.to_datetime(df[end_col],   dayfirst=True, errors="coerce")

    df = df.copy()
    df[new_col] = (end - start).dt.days
    return df


def CleanCustomers():
    Customers = pd.read_csv(INPUTCustomers)
    print(f"Loaded {len(Customers):,} rows from {INPUTCustomers.name}")

    #Remove Duplicates
    dupes = Customers.duplicated().sum()
    Customers = Customers.drop_duplicates()
    print (f"Removed {dupes:,} duplicate rows")

    #Remove Rows with missing values
    nulls = Customers.isna().any(axis=1).sum()
    Customers = Customers.dropna()
    print(f"Removed {nulls:,} rows with missing values")

    Customers = Customers.reset_index(drop=True)
    Customers.to_csv(OUTPUTCustomers, index=False, encoding="utf-8-sig")
    print(f"wrote {len(Customers):,} cleans rows to {OUTPUTCustomers}")
    print(Customers)

def CleanBooks():
    Books = pd.read_csv(INPUTBooks)
    print(f"Loaded {len(Books):,} rows from {INPUTBooks}")

    #Remove Duplicates
    dupes = Books.duplicated().sum()
    Books = Books.drop_duplicates()
    print (f"Removed {dupes:,} duplicate rows")

    #Remove Rows with missing values
    nulls = Books.isna().any(axis=1).sum()
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
    
    Books = days_between(Books, "book_checkout", "book_returned", "days_borrowed")


    Books = Books.reset_index(drop=True)
    Books.to_csv(OUTPUTBooks, index=False, encoding="utf-8-sig")
    print(f"wrote {len(Books):,} cleans rows to {OUTPUTBooks}")
    print(Books)


if __name__ == "__main__":
    CleanCustomers()
    CleanBooks()