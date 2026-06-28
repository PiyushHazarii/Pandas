"""
Day 05 - Time Series, Indexing & Resampling

Topics from the PDF:
- DatetimeIndex, PeriodIndex, date_range
- Date slicing and .dt accessors
- Resampling with ME, QE, YE, W, min
- Rolling, expanding, exponential moving averages
- Time zones, offsets, shift, pct_change
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from pandas.tseries.offsets import BDay, MonthEnd


def print_section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def show(label: str, value) -> None:
    print(f"\n--- {label} ---")
    print(value)


def make_daily_series() -> pd.Series:
    rng = np.random.default_rng(42)
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
    values = rng.normal(loc=100, scale=10, size=len(dates)).round(2)
    return pd.Series(values, index=dates, name="sales")


def datetimeindex_and_period() -> None:
    print_section("5.1 DatetimeIndex & Period")

    month_starts = pd.date_range(start="2024-01-01", periods=12, freq="MS")
    show("Month-start date_range", month_starts)

    ts = make_daily_series()
    show("Daily time series head", ts.head())
    show("Slice March 2024", ts["2024-03"].head())
    show("Slice Jan through Jun", ts["2024-01":"2024-06"].head())

    df = pd.DataFrame({"dt": pd.to_datetime(["2024-01-31 10:15", "2024-02-01 12:30"])})
    df["year"] = df["dt"].dt.year
    df["month"] = df["dt"].dt.month
    df["day"] = df["dt"].dt.day
    df["hour"] = df["dt"].dt.hour
    df["minute"] = df["dt"].dt.minute
    df["second"] = df["dt"].dt.second
    df["dayofweek"] = df["dt"].dt.dayofweek
    df["is_month_end"] = df["dt"].dt.is_month_end
    df["quarter"] = df["dt"].dt.quarter
    show("Datetime .dt attributes", df)

    pi = pd.period_range("2024-01", periods=12, freq="M")
    ps = pd.Series(range(12), index=pi, name="month_number")
    show("PeriodIndex Series", ps.head())
    show("Select first quarter from PeriodIndex", ps[ps.index.quarter == 1])


def resampling() -> None:
    print_section("5.2 Resampling")
    ts = make_daily_series()

    show("Monthly sum", ts.resample("ME").sum().head())
    show("Quarterly mean", ts.resample("QE").mean())
    show("Yearly max", ts.resample("YE").max())
    show("Weekly OHLC", ts.resample("W").ohlc().head())
    show("Monthly multiple aggregations", ts.resample("ME").agg(["sum", "mean", "count"]).head())

    ts_hourly = pd.Series(
        [10, 20, 15],
        index=pd.date_range("2024-01-01 00:00", periods=3, freq="h"),
        name="sensor",
    )
    show("Upsample hourly to per-minute with ffill", ts_hourly.resample("min").ffill().head(65))
    show(
        "Upsample hourly to per-minute with interpolation",
        ts_hourly.resample("min").interpolate(method="linear").head(65),
    )


def rolling_expanding() -> None:
    print_section("5.3 Rolling & Expanding Windows")
    ts = make_daily_series()

    show("7-day moving average", ts.rolling(window=7).mean().head(10))
    show("30-day rolling standard deviation", ts.rolling(window=30).std().head(35))
    show("7-day rolling sum with min_periods=3", ts.rolling(window=7, min_periods=3).sum().head(10))
    show("Exponential moving average with span=10", ts.ewm(span=10).mean().head())
    show("Exponential moving average with com=0.5", ts.ewm(com=0.5).mean().head())
    show("Expanding cumulative mean", ts.expanding().mean().head())
    show("Expanding running max", ts.expanding().max().head())
    show("14-day custom change", ts.rolling(14).apply(lambda values: values[-1] - values[0], raw=True).head(20))


def time_zones_offsets_shift() -> None:
    print_section("5.4 Time Zones & Offsets")
    ts = make_daily_series().head(5)

    ts_utc = ts.tz_localize("UTC")
    ts_ist = ts_utc.tz_convert("Asia/Kolkata")
    show("UTC localized Series", ts_utc)
    show("Converted to Asia/Kolkata", ts_ist)

    today = pd.Timestamp.today().normalize()
    next_bday = today + BDay(1)
    month_end = today + MonthEnd(0)
    show("Today", today)
    show("Next business day", next_bday)
    show("This month's end", month_end)

    show("Shift forward 1 period (lag)", ts.shift(1))
    show("Shift backward 1 period (lead)", ts.shift(-1))
    show("Period-over-period percent change", ts.pct_change())

    monthly = make_daily_series().resample("ME").sum()
    show("Year-over-year percent change for monthly data", monthly.pct_change(periods=12))


def main() -> None:
    pd.set_option("display.width", 120)
    pd.set_option("display.max_columns", 20)

    datetimeindex_and_period()
    resampling()
    rolling_expanding()
    time_zones_offsets_shift()


if __name__ == "__main__":
    main()

