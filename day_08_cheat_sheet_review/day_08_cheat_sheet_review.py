"""
Day 08 - Cheat Sheet Review

This file turns the PDF cheat sheet into one compact script. Run it after
Days 01-07 to quickly review the most important Pandas commands.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "generated_outputs"


def print_section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def show(label: str, value) -> None:
    print(f"\n--- {label} ---")
    print(value)


def make_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": ["001", "002", "003", "004", "005"],
            "city": ["Delhi", "Mumbai", "Delhi", "Pune", "Mumbai"],
            "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-02-01", "2024-02-10", "2024-03-01"]),
            "amount": [100.0, 200.0, np.nan, 150.0, 300.0],
            "qty": [1, 2, 1, 3, 2],
            "category": ["A", "B", "A", "B", "A"],
        }
    )


def import_setup_and_creation() -> pd.DataFrame:
    print_section("Import, Setup, and Creating Data")
    print("pandas version:", pd.__version__)
    pd.set_option("display.max_rows", 100)

    show("Series from list", pd.Series([1, 2, 3]))
    show("DataFrame from dict", pd.DataFrame({"a": [1, 2], "b": [3, 4]}))
    show("Date range", pd.date_range("2024-01", periods=12, freq="MS"))
    return make_dataframe()


def inspection_selection_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    print_section("Inspection, Selection, and Cleaning")

    show("shape", df.shape)
    show("dtypes", df.dtypes)
    print("\n--- info() ---")
    df.info()
    show("head", df.head(3))
    show("tail", df.tail(2))
    show("sample", df.sample(2, random_state=1))
    show("describe", df.describe(numeric_only=True))
    show("missing count", df.isna().sum())
    show("duplicate count", df.duplicated().sum())
    show("unique counts", df.nunique())
    show("value counts for city", df.value_counts("city"))

    show("Single column", df["city"])
    show("Multiple columns", df[["city", "amount"]])
    show("loc label selection", df.loc[0, "city"])
    show("iloc position selection", df.iloc[0, 3])
    show("Boolean filter", df[df["amount"] > 150])
    show("query filter", df.query('amount > 150 and city == "Mumbai"'))
    show("Fast scalar access with at", df.at[1, "amount"])
    show("Fast scalar access with iat", df.iat[1, 3])
    show("filter selected columns", df.filter(items=["id", "city"]))

    cleaned = df.copy()
    cleaned["amount"] = cleaned["amount"].fillna(0)
    cleaned["city"] = cleaned["city"].str.strip().str.lower()
    cleaned["category"] = cleaned["category"].astype("category")
    cleaned["id"] = cleaned["id"].astype("string")
    cleaned.drop_duplicates(subset=["id"], inplace=True)
    show("Cleaned data", cleaned)
    return cleaned


def manipulation_aggregation_time_series(df: pd.DataFrame) -> pd.DataFrame:
    print_section("Manipulation, Aggregation, and Time Series")

    changed = (
        df.rename(columns={"amount": "sales"})
        .assign(total=lambda x: x["sales"] * x["qty"])
        .sort_values("total", ascending=False)
        .reset_index(drop=True)
    )
    show("rename, assign, sort, reset_index", changed)
    show("set_index", changed.set_index("id"))

    extra = pd.DataFrame({"id": ["001", "002", "006"], "segment": ["retail", "online", "retail"]})
    show("concat vertically", pd.concat([changed.head(2), changed.tail(2)], ignore_index=True))
    show("merge left join", pd.merge(changed, extra, on="id", how="left"))

    show("groupby aggregate", changed.groupby("city")["sales"].agg(["sum", "mean"]))
    show("named aggregation", changed.groupby("city").agg(total_sales=("sales", "sum")))
    show("transform group mean", changed.groupby("city")["sales"].transform("mean"))
    show(
        "pivot table",
        changed.pivot_table(values="sales", index="city", columns="category", aggfunc="sum", fill_value=0),
    )
    show("melt wide to long", changed.melt(id_vars=["id"], value_vars=["sales", "qty"]))
    show("crosstab", pd.crosstab(changed["city"], changed["category"], normalize="index"))

    ts = changed.set_index("date").sort_index()["sales"]
    show("date parts", changed.assign(year=changed["date"].dt.year, month=changed["date"].dt.month))
    show("monthly resample", ts.resample("ME").sum())
    show("rolling mean", ts.rolling(2).mean())
    show("exponential moving average", ts.ewm(span=2).mean())
    show("shift and pct_change", pd.DataFrame({"lag": ts.shift(1), "pct_change": ts.pct_change()}))

    return changed


def output_and_performance(df: pd.DataFrame) -> None:
    print_section("Output and Performance")
    OUTPUT_DIR.mkdir(exist_ok=True)

    csv_path = OUTPUT_DIR / "cheat_sheet_output.csv"
    json_path = OUTPUT_DIR / "cheat_sheet_output.json"
    sqlite_path = OUTPUT_DIR / "cheat_sheet.sqlite"

    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", indent=2, date_format="iso")
    show("Saved CSV", csv_path)
    show("Saved JSON", json_path)

    try:
        xlsx_path = OUTPUT_DIR / "cheat_sheet_output.xlsx"
        df.to_excel(xlsx_path, index=False)
        show("Saved Excel", xlsx_path)
    except (ImportError, ModuleNotFoundError, ValueError) as exc:
        print("Excel output skipped. Install openpyxl to enable it.")
        print(f"Reason: {exc}")

    with sqlite3.connect(sqlite_path) as conn:
        df.to_sql("cheat_sheet", conn, if_exists="replace", index=False)
        show("Read back from SQL", pd.read_sql("SELECT * FROM cheat_sheet", conn))

    optimized = df.copy()
    optimized["city"] = optimized["city"].astype("category")
    optimized["qty"] = pd.to_numeric(optimized["qty"], downcast="integer")
    optimized["fast_total"] = optimized["sales"].values + optimized["qty"].values
    optimized["label"] = np.where(optimized["sales"] >= 200, "high", "normal")
    optimized.loc[optimized["sales"] == 0, "label"] = "missing"
    show("Performance-friendly operations", optimized)


def main() -> None:
    pd.set_option("display.width", 140)
    pd.set_option("display.max_columns", 30)

    df = import_setup_and_creation()
    cleaned = inspection_selection_cleaning(df)
    changed = manipulation_aggregation_time_series(cleaned)
    output_and_performance(changed)


if __name__ == "__main__":
    main()

