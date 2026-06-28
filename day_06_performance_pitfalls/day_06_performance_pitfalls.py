"""
Day 06 - Performance Tips & Common Pitfalls

Topics from the PDF:
- Vectorization vs Python loops
- Memory optimization with downcasting, category dtype, usecols, chunking
- SettingWithCopyWarning and safe assignment with .loc
- Common mistakes: integer index ambiguity, inplace confusion, axis confusion, slow groupby.apply
"""

from __future__ import annotations

from io import StringIO
from time import perf_counter

import numpy as np
import pandas as pd


def print_section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def show(label: str, value) -> None:
    print(f"\n--- {label} ---")
    print(value)


def vectorization_vs_loops() -> None:
    print_section("6.1 Vectorization vs Loops")

    rng = np.random.default_rng(42)
    n = 20_000
    df = pd.DataFrame({"a": rng.normal(size=n), "b": rng.normal(size=n)})

    start = perf_counter()
    loop_result = []
    for i in range(len(df)):
        loop_result.append(df["a"].iloc[i] + df["b"].iloc[i])
    loop_seconds = perf_counter() - start

    start = perf_counter()
    vectorized_result = df["a"] + df["b"]
    vectorized_seconds = perf_counter() - start

    start = perf_counter()
    numpy_result = df["a"].values + df["b"].values
    numpy_seconds = perf_counter() - start

    print(f"Loop time:       {loop_seconds:.6f} seconds")
    print(f"Vectorized time: {vectorized_seconds:.6f} seconds")
    print(f"NumPy time:      {numpy_seconds:.6f} seconds")
    show("First 5 loop results", loop_result[:5])
    show("First 5 vectorized results", vectorized_result.head())
    show("First 5 NumPy results", numpy_result[:5])

    df["flag_fast"] = np.where(df["a"] > 0, "pos", "neg")
    df["flag_slow"] = df["a"].apply(lambda x: "pos" if x > 0 else "neg")
    show("np.where vs apply produce same labels", df[["a", "flag_fast", "flag_slow"]].head())


def memory_optimization() -> None:
    print_section("6.2 Memory Optimization")

    df = pd.DataFrame(
        {
            "age": np.random.default_rng(1).integers(18, 70, size=1000),
            "score": np.random.default_rng(2).normal(75, 8, size=1000),
            "city": np.random.default_rng(3).choice(["Delhi", "Mumbai", "Pune"], size=1000),
            "status": np.random.default_rng(4).choice(["new", "active", "paused"], size=1000),
        }
    )

    before_mb = df.memory_usage(deep=True).sum() / 1024**2
    optimized = df.copy()
    optimized["age"] = pd.to_numeric(optimized["age"], downcast="integer")
    optimized["score"] = pd.to_numeric(optimized["score"], downcast="float")
    optimized["city"] = optimized["city"].astype("category")
    optimized["status"] = optimized["status"].astype("category")
    after_mb = optimized.memory_usage(deep=True).sum() / 1024**2

    print("\n--- df.info(memory_usage='deep') before optimization ---")
    df.info(memory_usage="deep")
    print("\n--- optimized.info(memory_usage='deep') ---")
    optimized.info(memory_usage="deep")
    print(f"\nMemory before: {before_mb:.4f} MB")
    print(f"Memory after:  {after_mb:.4f} MB")

    csv_text = """id,date,amount,region,unused
1,2024-01-01,100,North,x
2,2024-01-02,200,South,y
3,2024-01-03,300,North,z
4,2024-01-04,400,West,w
"""
    selected = pd.read_csv(StringIO(csv_text), usecols=["id", "date", "amount"])
    show("Read only needed columns with usecols", selected)

    chunk_source = StringIO(csv_text)
    results = []
    for chunk in pd.read_csv(chunk_source, chunksize=2):
        processed = chunk.groupby("region")["amount"].sum()
        results.append(processed)
    final = pd.concat(results).groupby(level=0).sum()
    show("Process CSV in chunks", final)


def settingwithcopywarning() -> None:
    print_section("6.3 SettingWithCopyWarning")

    df = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Carol", "Dave"],
            "city": ["Delhi", "Mumbai", "Delhi", "Pune"],
            "score": [88, 92, 79, 95],
        }
    )

    print("Problem pattern, shown as a comment:")
    print("subset = df[df['city'] == 'Delhi']")
    print("subset['score'] = 100  # may warn and may not modify original")

    subset = df[df["city"] == "Delhi"].copy()
    subset["score"] = 100
    show("Safe subset edit using .copy()", subset)
    show("Original DataFrame is unchanged", df)

    df.loc[df["city"] == "Delhi", "score"] = 100
    show("Safest original edit using .loc[condition, column]", df)

    pd.options.mode.copy_on_write = True
    print("\nCopy-on-Write option enabled for future-style behavior:")
    print(pd.options.mode.copy_on_write)


def other_common_pitfalls() -> None:
    print_section("6.4 Other Common Pitfalls")

    integer_label_df = pd.DataFrame({2: ["column label 2"], "value": [99]})
    show("df[2] selects column label 2, not row 2", integer_label_df[2])
    show("Use df.iloc[0] for row position 0", integer_label_df.iloc[0])

    axis_df = pd.DataFrame({"a": [1, 2], "b": [10, 20]})
    show("axis=0 gives column-wise result", axis_df.sum(axis=0))
    show("axis=1 gives row-wise result", axis_df.sum(axis=1))

    renamed = axis_df.rename(columns={"a": "alpha"})
    show("Prefer assigning method results instead of relying on inplace=True", renamed)

    grouped = pd.DataFrame(
        {
            "region": ["North", "North", "South", "South"],
            "sales": [100, 150, 90, 120],
        }
    )
    show("Fast built-in groupby aggregation", grouped.groupby("region")["sales"].sum())
    show("Slower groupby.apply equivalent", grouped.groupby("region").apply(lambda g: g["sales"].sum()))

    id_csv = StringIO("id,amount\n001,100\n002,200\n")
    inferred = pd.read_csv(id_csv)
    show("Pandas inferred ID as integer", inferred)

    id_csv = StringIO("id,amount\n001,100\n002,200\n")
    explicit = pd.read_csv(id_csv, dtype={"id": "string"})
    show("Explicit dtype keeps leading zeros", explicit)


def main() -> None:
    pd.set_option("display.width", 120)
    pd.set_option("display.max_columns", 20)

    vectorization_vs_loops()
    memory_optimization()
    settingwithcopywarning()
    other_common_pitfalls()


if __name__ == "__main__":
    main()

