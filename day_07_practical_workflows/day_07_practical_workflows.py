"""
Day 07 - Practical Examples & Common Workflows

Topics from the PDF:
- Exploratory Data Analysis pipeline
- Sales data analysis
- Data quality report
- Log file processing
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path

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


def quick_eda(df: pd.DataFrame) -> pd.DataFrame:
    print("Shape:", df.shape)
    print("\nDtypes:\n", df.dtypes)
    print("\nMissing values:\n", df.isna().sum())
    print("\nDuplicate rows:", df.duplicated().sum())
    print("\nNumeric summary:\n", df.describe(numeric_only=True))
    print("\nCategorical columns:")
    for col in df.select_dtypes("object").columns:
        mode = df[col].mode(dropna=True)
        top = mode.iloc[0] if not mode.empty else None
        print(f"{col}: {df[col].nunique(dropna=True)} unique | top={top}")
    return df


def make_sales_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": [1001, 1002, 1002, 1003, 1004, 1005, None],
            "customer_id": ["C001", "C002", "C002", "C001", "C003", "C004", "C005"],
            "order_date": [
                "2024-01-05",
                "2024-01-08",
                "2024-01-08",
                "2024-02-12",
                "2024-02-15",
                "2024-03-01",
                "2024-03-03",
            ],
            "region": ["North", "West", "West", "North", "South", "West", "South"],
            "category": ["Books", "Games", "Games", "Books", "Tools", "Games", "Books"],
            "amount": ["250.50", "499.00", "499.00", "175.25", "800.00", "299.99", None],
        }
    )


def eda_pipeline() -> pd.DataFrame:
    print_section("7.1 Exploratory Data Analysis Pipeline")
    df = make_sales_dataframe()
    return quick_eda(df)


def sales_data_analysis(raw_df: pd.DataFrame) -> pd.DataFrame:
    print_section("7.2 Sales Data Analysis")

    df = raw_df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df.dropna(subset=["order_id", "amount"], inplace=True)
    df.drop_duplicates(subset=["order_id"], inplace=True)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df.dropna(subset=["amount"], inplace=True)
    df["year_month"] = df["order_date"].dt.to_period("M")

    monthly = df.groupby("year_month")["amount"].sum().reset_index()
    monthly["mom_growth"] = monthly["amount"].pct_change() * 100
    show("Monthly revenue trend", monthly)

    top_customers = (
        df.groupby("customer_id")
        .agg(total=("amount", "sum"), orders=("order_id", "count"))
        .sort_values("total", ascending=False)
        .head(5)
    )
    show("Top 5 customers by revenue", top_customers)

    pivot = df.pivot_table(
        values="amount",
        index="region",
        columns="category",
        aggfunc="sum",
        fill_value=0,
    )
    show("Revenue by region and category", pivot)

    df_ts = df.set_index("order_date").sort_index()
    df_ts["rolling_30d"] = df_ts["amount"].rolling("30D").mean()
    show("30-day rolling average", df_ts[["amount", "rolling_30d"]])

    return df


def data_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    report = pd.DataFrame(index=df.columns)
    report["dtype"] = df.dtypes.astype(str)
    report["non_null"] = df.notna().sum()
    report["null_count"] = df.isna().sum()
    report["null_pct"] = (df.isna().mean() * 100).round(2)
    report["unique"] = df.nunique(dropna=True)
    report["unique_pct"] = (df.nunique(dropna=True) / len(df) * 100).round(2)
    report["duplicates"] = df.duplicated().sum()

    for col in df.select_dtypes(include="number"):
        report.loc[col, "min"] = df[col].min()
        report.loc[col, "max"] = df[col].max()
        report.loc[col, "mean"] = round(df[col].mean(), 2)

    return report


def data_quality_workflow(df: pd.DataFrame) -> None:
    print_section("7.3 Data Quality Report")
    quality_df = data_quality_report(df)
    show("Data quality report", quality_df)

    OUTPUT_DIR.mkdir(exist_ok=True)
    xlsx_path = OUTPUT_DIR / "data_quality.xlsx"
    csv_path = OUTPUT_DIR / "data_quality.csv"

    try:
        quality_df.to_excel(xlsx_path)
        show("Saved Excel report", xlsx_path)
    except (ImportError, ModuleNotFoundError, ValueError) as exc:
        quality_df.to_csv(csv_path)
        print("Excel report skipped. CSV report was written instead.")
        print(f"Reason: {exc}")
        show("Saved CSV report", csv_path)


def log_file_processing() -> None:
    print_section("7.4 Log File Processing")

    raw_logs = """2024-01-01 10:00:00 | INFO | user=101 path=/home loaded
2024-01-01 10:05:00 | ERROR | user=102 path=/checkout failed
2024-01-01 10:15:00 | ERROR | user=103 path=/checkout timeout
2024-01-01 11:00:00 | INFO | user=101 path=/orders loaded
2024-01-01 11:10:00 | ERROR | user=104 path=/login failed
"""
    logs = pd.read_csv(
        StringIO(raw_logs),
        sep="|",
        header=None,
        names=["timestamp", "level", "message"],
    )
    logs["timestamp"] = pd.to_datetime(logs["timestamp"].str.strip())
    logs["level"] = logs["level"].str.strip()
    logs["message"] = logs["message"].str.strip()

    logs["user_id"] = logs["message"].str.extract(r"user=(\d+)")
    logs["endpoint"] = logs["message"].str.extract(r"path=([^\s]+)")
    logs["hour"] = logs["timestamp"].dt.floor("h")
    show("Parsed logs", logs)

    error_rate = (
        logs.assign(is_error=logs["level"].eq("ERROR"))
        .groupby("hour")["is_error"]
        .mean()
        .mul(100)
        .rename("error_pct")
    )
    show("Error rate per hour", error_rate)
    show(
        "Top error endpoints",
        logs[logs["level"] == "ERROR"]["endpoint"].value_counts().head(10),
    )


def main() -> None:
    pd.set_option("display.width", 140)
    pd.set_option("display.max_columns", 30)

    raw_df = eda_pipeline()
    cleaned_sales = sales_data_analysis(raw_df)
    data_quality_workflow(cleaned_sales)
    log_file_processing()


if __name__ == "__main__":
    main()

