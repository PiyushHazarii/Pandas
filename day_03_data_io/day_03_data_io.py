"""
Day 03 - Data I/O

Topics from the PDF:
- CSV: read_csv, to_csv, selected columns, dtypes, dates, na_values, chunksize
- Excel: read_excel, to_excel, ExcelWriter
- JSON: read_json, to_json, json_normalize
- SQL: read_sql, read_sql_query, to_sql
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pandas as pd
from pandas import json_normalize


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "generated_outputs"


def print_section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def show(label: str, value) -> None:
    print(f"\n--- {label} ---")
    print(value)


def make_sales_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": [1001, 1002, 1003, 1004, 1005],
            "customer_id": ["C001", "C002", "C001", "C003", "C004"],
            "order_date": pd.to_datetime(
                ["2024-01-05", "2024-01-08", "2024-02-12", "2024-02-15", "2024-03-01"]
            ),
            "region": ["North", "West", "North", "South", "West"],
            "category": ["Books", "Games", "Books", "Tools", "Games"],
            "amount": [250.5, 499.0, 175.25, 800.0, 299.99],
        }
    )


def csv_examples(df: pd.DataFrame) -> None:
    print_section("3.1 CSV")
    csv_path = OUTPUT_DIR / "sales.csv"
    selected_path = OUTPUT_DIR / "sales_selected.csv"

    df.to_csv(csv_path, index=False)
    show("Wrote CSV file", csv_path)

    loaded = pd.read_csv(
        csv_path,
        sep=",",
        header=0,
        usecols=["order_id", "customer_id", "order_date", "amount"],
        dtype={"customer_id": "string"},
        na_values=["NA", "N/A", "--"],
        parse_dates=["order_date"],
        encoding="utf-8",
        nrows=1000,
    )
    show("Read CSV with key parameters", loaded)
    show("Loaded dtypes", loaded.dtypes)

    df.to_csv(selected_path, index=False, columns=["customer_id", "amount"], float_format="%.2f")
    show("Write only selected columns with formatted floats", selected_path)

    big_path = OUTPUT_DIR / "big_sales.csv"
    big_df = pd.concat([df] * 4, ignore_index=True)
    big_df.to_csv(big_path, index=False)

    chunks = pd.read_csv(big_path, chunksize=5)
    combined = pd.concat([chunk for chunk in chunks], ignore_index=True)
    show("Chunked read, then concat", combined.head(8))


def excel_examples(df: pd.DataFrame) -> None:
    print_section("3.2 Excel")
    xlsx_path = OUTPUT_DIR / "sales_report.xlsx"

    try:
        df.to_excel(xlsx_path, index=False, sheet_name="Sales")
        loaded = pd.read_excel(xlsx_path, sheet_name="Sales")
        show("Read Excel sheet by name", loaded)

        multi_path = OUTPUT_DIR / "multi_sheet_report.xlsx"
        with pd.ExcelWriter(multi_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Sales", index=False)
            df.groupby("region", as_index=False)["amount"].sum().to_excel(
                writer,
                sheet_name="RegionSummary",
                index=False,
            )
        show("Wrote multiple sheets", multi_path)
    except (ImportError, ModuleNotFoundError, ValueError) as exc:
        print("Excel example skipped. Install openpyxl to run it.")
        print(f"Reason: {exc}")


def json_examples(df: pd.DataFrame) -> None:
    print_section("3.3 JSON")
    json_path = OUTPUT_DIR / "sales.json"

    df.to_json(json_path, orient="records", indent=2, date_format="iso")
    show("Write JSON records", json_path)
    show("Read JSON records", pd.read_json(json_path, orient="records"))

    nested_data = [
        {
            "customer_id": "C001",
            "date": "2024-01-05",
            "orders": [
                {"order_id": 1001, "amount": 250.5},
                {"order_id": 1003, "amount": 175.25},
            ],
        },
        {
            "customer_id": "C002",
            "date": "2024-01-08",
            "orders": [{"order_id": 1002, "amount": 499.0}],
        },
    ]
    nested_path = OUTPUT_DIR / "nested_sales.json"
    nested_path.write_text(json.dumps(nested_data, indent=2), encoding="utf-8")

    flattened = json_normalize(nested_data, record_path="orders", meta=["customer_id", "date"])
    show("Flatten nested JSON with json_normalize", flattened)


def sql_examples(df: pd.DataFrame) -> None:
    print_section("3.4 SQL Databases")
    sqlite_path = OUTPUT_DIR / "sales.sqlite"

    with sqlite3.connect(sqlite_path) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)

        show("Read whole table with SQL", pd.read_sql("SELECT * FROM sales", conn))
        show(
            "Read filtered SQL query",
            pd.read_sql_query("SELECT order_id, customer_id, amount FROM sales WHERE amount > 300", conn),
        )

        summary = df.groupby("region", as_index=False)["amount"].sum()
        summary.to_sql("region_summary", conn, if_exists="replace", index=False)
        show("Read table written by to_sql", pd.read_sql("SELECT * FROM region_summary", conn))


def main() -> None:
    pd.set_option("display.width", 120)
    pd.set_option("display.max_columns", 20)
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = make_sales_dataframe()
    csv_examples(df)
    excel_examples(df)
    json_examples(df)
    sql_examples(df)


if __name__ == "__main__":
    main()

