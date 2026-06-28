"""
Day 02 - Data Cleaning & Preprocessing

Topics from the PDF:
- Missing values: isna, notna, dropna, fillna, ffill, bfill, interpolate
- Duplicates: duplicated, drop_duplicates
- Type conversions: astype, pd.to_numeric, pd.to_datetime
- String operations through the .str accessor
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def print_section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def show(label: str, value) -> None:
    print(f"\n--- {label} ---")
    print(value)


def make_messy_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": [" Alice ", "Bob", "Carol", "Bob", None, "Eve"],
            "age": ["25", "30", None, "30", "bad", "41"],
            "score": [88.5, np.nan, 78.3, np.nan, 91.0, 85.5],
            "city": ["Delhi", "Mumbai", None, "Mumbai", "Pune", "Delhi"],
            "email": [
                " Alice@Example.com ",
                "bob@example.com",
                "carol@example.com",
                "bob@example.com",
                None,
                "eve example.com",
            ],
            "date": ["01/01/2024", "03/01/2024", None, "03/01/2024", "bad", "10/01/2024"],
        }
    )


def missing_values() -> None:
    print_section("2.1 Missing Values")
    df = make_messy_dataframe()
    show("Raw messy data", df)

    show("df.isna()", df.isna())
    show("Missing count per column", df.isna().sum())
    show("Missing percent per column", (df.isna().sum() / len(df) * 100).round(2))
    show("df.notna()", df.notna())

    show("Drop rows with any missing value", df.dropna())
    show("Drop rows where all values are missing", df.dropna(how="all"))
    show("Drop rows only when age or score is missing", df.dropna(subset=["age", "score"]))
    show("Drop columns with any missing value", df.dropna(axis=1))
    show("Keep rows with at least 4 non-missing values", df.dropna(thresh=4))

    filled = df.fillna({"age": "0", "score": df["score"].median(), "city": "Unknown"})
    show("Fill selected columns with useful defaults", filled)

    show("Forward fill", df.ffill())
    show("Backward fill", df.bfill())
    show("Forward fill at most 2 consecutive missing values", df.ffill(limit=2))

    show("Linear interpolation on score", df["score"].interpolate(method="linear"))

    dated_scores = pd.Series(
        [10.0, np.nan, np.nan, 40.0],
        index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-04", "2024-01-07"]),
    )
    show("Time interpolation with DatetimeIndex", dated_scores.interpolate(method="time"))


def duplicates() -> None:
    print_section("2.2 Duplicates")
    df = make_messy_dataframe()

    show("Duplicate mask for entire rows", df.duplicated())
    show("Number of duplicate rows", df.duplicated().sum())
    show("All duplicate rows", df[df.duplicated(keep=False)])
    show(
        "Duplicates based on name and city",
        df.duplicated(subset=["name", "city"], keep="first"),
    )
    show("Drop duplicate rows", df.drop_duplicates())
    show("Drop duplicates keeping last", df.drop_duplicates(keep="last"))
    show("Drop duplicate emails", df.drop_duplicates(subset=["email"]))


def type_conversions() -> None:
    print_section("2.3 Type Conversions")
    df = make_messy_dataframe()

    show("Original dtypes", df.dtypes)

    cleaned = df.copy()
    cleaned["age"] = pd.to_numeric(cleaned["age"], errors="coerce").astype("Int64")
    cleaned["score"] = cleaned["score"].astype(float)
    cleaned["city"] = cleaned["city"].astype("category")
    cleaned["date"] = pd.to_datetime(cleaned["date"], format="%d/%m/%Y", errors="coerce")

    show("Converted dtypes", cleaned.dtypes)
    show("Cleaned values after safe conversion", cleaned)

    cleaned["year"] = cleaned["date"].dt.year
    cleaned["month"] = cleaned["date"].dt.month
    cleaned["day_name"] = cleaned["date"].dt.day_name()
    show("Extract datetime parts", cleaned[["date", "year", "month", "day_name"]])


def string_operations() -> None:
    print_section("2.4 String Operations")
    df = make_messy_dataframe()
    s = df["name"]

    show("Lowercase", s.str.lower())
    show("Uppercase", s.str.upper())
    show("Strip spaces", s.str.strip())
    show("Replace text", s.str.replace("Bob", "Robert", regex=False))
    show("Contains 'Al'", s.str.contains("Al", na=False))
    show("Starts with A after stripping", s.str.strip().str.startswith("A", na=False))
    show("Split email at @", df["email"].str.split("@"))
    show("Split email into columns", df["email"].str.split("@", expand=True))
    show("Extract numbers from age", df["age"].astype("string").str.extract(r"(\d+)"))
    show("String lengths", s.str.len())
    show("Count letter a", s.str.lower().str.count("a"))
    show("Join all non-missing names", s.dropna().str.strip().str.cat(sep=", "))

    cleaned_email = (
        df["email"]
        .str.lower()
        .str.strip()
        .str.replace(" ", "_", regex=False)
    )
    show("Chained email cleanup", cleaned_email)


def main() -> None:
    pd.set_option("display.width", 120)
    pd.set_option("display.max_columns", 20)

    missing_values()
    duplicates()
    type_conversions()
    string_operations()


if __name__ == "__main__":
    main()

