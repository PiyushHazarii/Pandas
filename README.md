# Pandas Complete Study Guide - Day-wise Code Practice

This repository converts the notes from `D:\Pandas_Complete_Study_Guide.pdf` into a structured, day-wise Pandas learning project. The goal is simple: do not just read Pandas concepts, run them, modify them, and understand why each command behaves the way it does.

Every day folder contains one focused Python script with self-contained sample data. You do not need external datasets to begin. The examples are intentionally small, readable, and practical so you can connect each line of code back to the PDF topics.

## Project Goals

- Build a strong foundation in Pandas using runnable examples.
- Learn the most important Pandas APIs in a logical order.
- Practice real data workflows: cleaning, loading, joining, grouping, reshaping, time series, performance, and reporting.
- Keep each lesson independent so you can revise any day without breaking the others.
- Make the code beginner-friendly while still following professional Python habits.

## Repository Structure

```text
Pandas/
|-- README.md
|-- requirements.txt
|-- day_01_pandas_fundamentals/
|   `-- day_01_pandas_fundamentals.py
|-- day_02_data_cleaning/
|   `-- day_02_data_cleaning.py
|-- day_03_data_io/
|   `-- day_03_data_io.py
|-- day_04_data_manipulation/
|   `-- day_04_data_manipulation.py
|-- day_05_time_series/
|   `-- day_05_time_series.py
|-- day_06_performance_pitfalls/
|   `-- day_06_performance_pitfalls.py
|-- day_07_practical_workflows/
|   `-- day_07_practical_workflows.py
`-- day_08_cheat_sheet_review/
    `-- day_08_cheat_sheet_review.py
```

## Prerequisites

Use Python 3.10 or newer.

Check Python:

```powershell
python --version
```

If the command is not found, install Python from the official Python website and make sure `Add Python to PATH` is selected during installation.

## Setup

Open PowerShell inside this project folder:

```powershell
cd C:\Users\Asus\Videos\Pandas
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

The dependencies are intentionally minimal:

| Package | Why It Is Used |
| --- | --- |
| `pandas` | Main data analysis library |
| `numpy` | Numeric arrays, random sample data, vectorized operations |
| `openpyxl` | Excel read/write support for `.xlsx` files |

## How To Run

Run one day at a time. Start with Day 01:

```powershell
python .\day_01_pandas_fundamentals\day_01_pandas_fundamentals.py
```

Then continue with Day 02:

```powershell
python .\day_02_data_cleaning\day_02_data_cleaning.py
```

You can run any day independently because each script creates its own sample data.

## Curriculum Roadmap

| Day | Folder | Main Focus | You Will Learn |
| --- | --- | --- | --- |
| 01 | `day_01_pandas_fundamentals` | Pandas basics | Series, DataFrames, attributes, indexing, selection, modifying data |
| 02 | `day_02_data_cleaning` | Cleaning messy data | Missing values, duplicates, type conversion, datetime parsing, string cleanup |
| 03 | `day_03_data_io` | Reading and writing data | CSV, Excel, JSON, SQLite SQL, chunked file processing |
| 04 | `day_04_data_manipulation` | Combining and reshaping | merge, join, concat, groupby, pivot tables, melt, crosstab, vectorization |
| 05 | `day_05_time_series` | Date and time data | DatetimeIndex, PeriodIndex, resampling, rolling windows, time zones, offsets |
| 06 | `day_06_performance_pitfalls` | Writing better Pandas | Vectorization, memory optimization, safe assignment, common beginner mistakes |
| 07 | `day_07_practical_workflows` | Real workflows | EDA pipeline, sales analysis, data quality report, log processing |
| 08 | `day_08_cheat_sheet_review` | Revision | Essential Pandas commands from the cheat sheet in one compact script |

## Recommended Study Method

1. Run the script for the current day.
2. Read the output slowly from top to bottom.
3. Open the `.py` file and compare each output with the code that produced it.
4. Change a few values in the sample data.
5. Run the script again and predict the result before looking at the output.
6. Add one small exercise of your own at the bottom of the file.

This is the fastest way to move from "I have seen this command" to "I understand when and why to use this command".

## Generated Outputs

Some days create output files so you can practice real save/load workflows.

| Day | Output Location | Examples |
| --- | --- | --- |
| Day 03 | `day_03_data_io/generated_outputs/` | CSV, Excel, JSON, SQLite files |
| Day 07 | `day_07_practical_workflows/generated_outputs/` | Data quality report |
| Day 08 | `day_08_cheat_sheet_review/generated_outputs/` | CSV, JSON, Excel, SQLite review files |

These generated files are learning artifacts. It is safe to delete them and rerun the scripts.

## Coding Style Used In This Project

The scripts follow a consistent structure:

- `print_section()` separates major topics in terminal output.
- `show()` prints a label and result together so output is easy to understand.
- Sample data is created inside helper functions such as `make_sales_dataframe()`.
- Each major topic has its own function.
- `main()` controls the lesson flow.
- `if __name__ == "__main__":` allows each script to run directly.

This keeps the code readable now and easier to extend later.

## Common Commands

Run Day 01:

```powershell
python .\day_01_pandas_fundamentals\day_01_pandas_fundamentals.py
```

Run Day 03:

```powershell
python .\day_03_data_io\day_03_data_io.py
```

Run Day 07:

```powershell
python .\day_07_practical_workflows\day_07_practical_workflows.py
```

Upgrade dependencies if needed:

```powershell
python -m pip install --upgrade -r requirements.txt
```

Deactivate the virtual environment:

```powershell
deactivate
```

## Troubleshooting

### `python` is not recognized

Python is not installed or not added to PATH. Install Python 3.10 or newer and reopen PowerShell.

### `ModuleNotFoundError: No module named 'pandas'`

The virtual environment is not active, or dependencies are not installed.

Run:

```powershell
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Excel examples do not run

Install `openpyxl`:

```powershell
pip install openpyxl
```

It is already included in `requirements.txt`, so this usually means dependencies were not installed.

### Output looks too wide in the terminal

The scripts already set Pandas display width, but some outputs can still be large. Maximize the terminal window or run the file inside VS Code's terminal.

## Suggested Practice Exercises

After each day, try these:

- Add one new row to the sample DataFrame.
- Add one new column and calculate something from existing columns.
- Filter the data using one extra condition.
- Sort the result in a different order.
- Save one output to CSV and read it back.
- Write down one mistake you made and the corrected version.

## Learning Outcome

After completing all 8 days, you should be comfortable with:

- Creating and inspecting Series and DataFrames.
- Selecting rows and columns correctly with `loc`, `iloc`, boolean masks, and `query`.
- Cleaning missing, duplicate, badly typed, and messy string data.
- Reading and writing CSV, Excel, JSON, and SQL data.
- Combining datasets with `merge`, `join`, and `concat`.
- Aggregating data with `groupby`, `pivot_table`, and `crosstab`.
- Working with dates, resampling, rolling windows, and time zones.
- Avoiding slow loops, chained indexing, dtype mistakes, and common Pandas pitfalls.
- Building small end-to-end analysis workflows.

## Notes

This project is designed for learning, so clarity is preferred over cleverness. Once you understand the examples, you can refactor them into notebooks, reusable modules, or larger real-world projects.
