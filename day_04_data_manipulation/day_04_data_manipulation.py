"""
Day 04 - Data Manipulation

Topics from the PDF:
- merge, join, concat
- GroupBy: split, apply, combine
- pivot_table, pivot, melt, crosstab
- apply, map, vectorized operations, cut, qcut
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


def make_people_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "name": ["Alice", "Bob", "Carol", "Dave"],
            "dept": ["D1", "D2", "D1", "D3"],
            "city": ["Delhi", "Mumbai", "Pune", "Delhi"],
            "year": [2024, 2024, 2025, 2025],
            "score": [88.5, 92.0, 78.3, 95.1],
            "revenue": [1200, 1800, 950, 2200],
        }
    )


def merge_join_concat() -> None:
    print_section("4.1 Merge, Join & Concat")

    employees = make_people_dataframe()
    departments = pd.DataFrame(
        {
            "dept_code": ["D1", "D2", "D4"],
            "department": ["Analytics", "Sales", "Support"],
        }
    )
    reviews = pd.DataFrame(
        {
            "employee_id": [1, 2, 2, 5],
            "review": ["Strong", "Good", "Promotion-ready", "New hire"],
        }
    )

    show("Employees", employees)
    show("Departments", departments)
    show("Reviews with duplicate employee_id", reviews)

    show(
        "Inner merge on employee_id",
        pd.merge(employees, reviews, on="employee_id", how="inner"),
    )
    show(
        "Left merge with different key names",
        pd.merge(employees, departments, left_on="dept", right_on="dept_code", how="left"),
    )
    show(
        "Outer merge with indicator",
        pd.merge(employees, reviews, on="employee_id", how="outer", indicator=True),
    )
    show(
        "Merge on multiple columns",
        pd.merge(
            employees,
            employees[["dept", "year", "revenue"]].rename(columns={"revenue": "dept_year_revenue"}),
            on=["dept", "year"],
            how="left",
        ),
    )

    result = pd.merge(employees, reviews, on="employee_id", how="left")
    print(f"\nRow check after merge: left rows={len(employees)}, result rows={len(result)}")
    print("If result rows are larger, check for duplicate join keys.")

    df1 = employees.iloc[:2]
    df2 = employees.iloc[2:]
    show("Vertical concat", pd.concat([df1, df2], ignore_index=True))
    show("Horizontal concat", pd.concat([employees[["name"]], employees[["score"]]], axis=1))

    left_indexed = employees.set_index("employee_id")
    right_indexed = reviews.drop_duplicates("employee_id").set_index("employee_id")
    show("Index-based join", left_indexed.join(right_indexed, how="left"))


def groupby_examples() -> None:
    print_section("4.2 GroupBy - Split, Apply, Combine")
    df = make_people_dataframe()

    show("Mean score per city", df.groupby("city")["score"].mean())
    show(
        "Multiple aggregations",
        df.groupby("city")["score"].agg(["mean", "max", "min", "count"]),
    )
    show("Revenue by city and year", df.groupby(["city", "year"])["revenue"].sum())

    named = df.groupby("city").agg(
        avg_score=("score", "mean"),
        max_score=("score", "max"),
        total_revenue=("revenue", "sum"),
        n_rows=("name", "count"),
    )
    show("Named aggregations", named)

    show("Custom score range per city", df.groupby("city")["score"].agg(lambda x: x.max() - x.min()))

    df["score_z"] = df.groupby("city")["score"].transform(
        lambda x: (x - x.mean()) / x.std(ddof=0) if len(x) > 1 else 0
    )
    show("transform() returns same-shape group result", df[["name", "city", "score", "score_z"]])

    show("filter() keeps groups where mean score > 85", df.groupby("city").filter(lambda g: g["score"].mean() > 85))

    print("\n--- Iterate over groups ---")
    for city, group_df in df.groupby("city"):
        print(city, group_df.shape)


def pivot_and_reshape() -> None:
    print_section("4.3 Pivot Tables & Crosstabs")

    sales = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02"]),
            "region": ["North", "North", "South", "South"],
            "product": ["A", "B", "A", "B"],
            "sales": [100, 150, 120, 90],
            "grade": ["High", "High", "Low", "Low"],
            "Q1": [10, 15, 12, 9],
            "Q2": [20, 25, 22, 19],
        }
    )

    show(
        "pivot_table with totals",
        sales.pivot_table(
            values="sales",
            index="region",
            columns="product",
            aggfunc="sum",
            fill_value=0,
            margins=True,
            margins_name="Total",
        ),
    )
    show("pivot without aggregation", sales.pivot(index="date", columns="product", values="sales"))
    show(
        "melt from wide to long",
        sales.melt(
            id_vars=["date", "region"],
            value_vars=["Q1", "Q2"],
            var_name="quarter",
            value_name="sales_value",
        ),
    )
    show("crosstab normalized by row", pd.crosstab(sales["region"], sales["grade"], normalize="index"))


def apply_map_vectorized() -> None:
    print_section("4.4 apply(), map(), and Vectorized Operations")
    df = make_people_dataframe()

    show("apply per column", df[["score", "revenue"]].apply(lambda x: x.max() - x.min(), axis=0))
    show("apply per row", df.apply(lambda row: row["score"] * 2, axis=1))

    df["grade_from_map"] = df["score"].map(lambda x: "A" if x >= 90 else "B")
    show("map element-wise on a Series", df[["name", "score", "grade_from_map"]])

    df["discounted_revenue"] = df["revenue"] * 0.90
    df["total"] = df["score"] * df["revenue"]
    df["label"] = np.where(df["score"] >= 90, "A", "B")
    show("Vectorized columns", df[["name", "discounted_revenue", "total", "label"]])

    df["band"] = pd.cut(df["score"], bins=[0, 60, 80, 90, 100], labels=["C", "B", "A-", "A"])
    df["qband"] = pd.qcut(df["score"], q=4, labels=["Q1", "Q2", "Q3", "Q4"])
    show("cut and qcut", df[["name", "score", "band", "qband"]])


def main() -> None:
    pd.set_option("display.width", 140)
    pd.set_option("display.max_columns", 30)

    merge_join_concat()
    groupby_examples()
    pivot_and_reshape()
    apply_map_vectorized()


if __name__ == "__main__":
    main()

