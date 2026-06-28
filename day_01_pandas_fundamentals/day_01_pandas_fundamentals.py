"""
Day 01 - Pandas Fundamentals

Topics from the PDF:
- Series creation, attributes, access, vectorized operations, alignment
- DataFrame creation from dicts, lists, and NumPy arrays
- DataFrame inspection with shape, dtypes, info, describe, head, tail, sample
- Indexing and selection with loc, iloc, boolean masks, query, at, iat
- Modifying DataFrames with assign, rename, drop, reset_index, set_index, sort
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
            "name": ["Alice", "Bob", "Carol", "Dave"],
            "age": [25, 30, 35, 28],
            "score": [88.5, 92.0, 78.3, 95.1],
            "city": ["Delhi", "Mumbai", "Pune", "Delhi"],
        }
    )


def series_basics() -> None:
    print_section("1.1 Series - The 1-D Building Block")

    s1 = pd.Series([10, 20, 30, 40])
    s2 = pd.Series([10, 20, 30], index=["a", "b", "c"])
    s3 = pd.Series({"x": 100, "y": 200})
    s4 = pd.Series(5, index=range(4))

    show("Series from list with default index", s1)
    show("Series with custom index", s2)
    show("Series from dict", s3)
    show("Scalar broadcast into a Series", s4)

    show("s2.values", s2.values)
    show("s2.index", s2.index)
    show("s2.dtype", s2.dtype)
    show("s2.shape", s2.shape)
    show("s2.name before setting", s2.name)
    s2.name = "score"
    show("s2.name after setting", s2.name)

    show("Label-based access with .loc['b']", s2.loc["b"])
    show("Position-based access with .iloc[1]", s2.iloc[1])
    show("Fancy indexing with labels ['a', 'c']", s2.loc[["a", "c"]])

    show("Vectorized multiplication", s2 * 2)
    show("Boolean mask", s2 > 15)
    show("Filtered Series", s2[s2 > 15])

    other = pd.Series([1, 2, 3], index=["b", "c", "d"])
    show("Automatic alignment on index labels", s2 + other)


def dataframe_basics() -> None:
    print_section("1.2 DataFrame - The 2-D Table")

    df = make_people_dataframe()
    df2 = pd.DataFrame([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
    df3 = pd.DataFrame(
        np.random.default_rng(42).normal(size=(4, 3)),
        columns=["X", "Y", "Z"],
    )

    show("DataFrame from dict of lists", df)
    show("DataFrame from list of dicts", df2)
    show("DataFrame from NumPy array", df3)

    show("df.shape", df.shape)
    show("df.dtypes", df.dtypes)
    show("df.columns", df.columns)
    show("df.index", df.index)
    print("\n--- df.info() ---")
    df.info()
    show("df.describe()", df.describe())
    show("df.head(2)", df.head(2))
    show("df.tail(2)", df.tail(2))
    show("df.sample(2, random_state=1)", df.sample(2, random_state=1))


def indexing_and_selection() -> None:
    print_section("1.3 Indexing & Selection")
    df = make_people_dataframe()

    show("df.loc[0] - row with label 0", df.loc[0])
    show("df.loc[0:2] - label slice includes 2", df.loc[0:2])
    show("df.loc[0, 'name'] - single cell by label", df.loc[0, "name"])
    show("df.loc[0:2, 'name':'score']", df.loc[0:2, "name":"score"])

    show("df.iloc[0] - first row by position", df.iloc[0])
    show("df.iloc[0:2] - position slice excludes 2", df.iloc[0:2])
    show("df.iloc[0, 1] - row 0, column 1", df.iloc[0, 1])
    show("df.iloc[:, 1:3] - all rows, columns 1 and 2", df.iloc[:, 1:3])

    show("Rows where age > 28", df[df["age"] > 28])
    show(
        "Rows where age > 25 and city == Delhi",
        df[(df["age"] > 25) & (df["city"] == "Delhi")],
    )
    show("query() syntax", df.query('age > 28 and city == "Delhi"'))

    show("df['name'] returns a Series", df["name"])
    show("df[['name', 'score']] returns a DataFrame", df[["name", "score"]])
    show("df.at[2, 'score'] - fast scalar by label", df.at[2, "score"])
    show("df.iat[2, 2] - fast scalar by position", df.iat[2, 2])


def modifying_dataframes() -> None:
    print_section("1.4 Modifying DataFrames")
    df = make_people_dataframe()

    df["grade"] = df["score"].apply(lambda x: "A" if x >= 90 else "B")
    show("Add a grade column", df)

    renamed = df.rename(columns={"score": "marks", "city": "location"})
    show("Rename columns", renamed)

    without_grade = df.drop(columns=["grade"])
    show("Drop a column", without_grade)

    without_first_two = df.drop(index=[0, 1])
    show("Drop rows by label", without_first_two)

    reset = without_first_two.reset_index(drop=True)
    show("Reset index after dropping rows", reset)

    indexed = df.set_index("name")
    show("Set name as index", indexed)
    show("Sort by age descending", df.sort_values("age", ascending=False))
    show("Sort by row labels", indexed.sort_index())

    assigned = df.assign(
        bonus=df["score"] * 0.10,
        rank=df["score"].rank(ascending=False),
    )
    show("assign() creates new columns in a chain-friendly way", assigned)


def main() -> None:
    pd.set_option("display.width", 120)
    pd.set_option("display.max_columns", 20)

    series_basics()
    dataframe_basics()
    indexing_and_selection()
    modifying_dataframes()


if __name__ == "__main__":
    main()

