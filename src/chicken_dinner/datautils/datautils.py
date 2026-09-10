"""
I wanted to use Pandas here, since it is the best tool for the job.
Of course, we can do this with the Standardlib as well. But I reasoned
that Pandas was the right choice.

The thing that differs from stdlib is that I would have used the
internal csv package for reading and/or writing. I would probably have
made Pydantic types, dataclasses or pure objects from scratch.

But for this project Pandas is fine.
"""

import pandas as pd
from os import path


def load_csv(path_to_file: str) -> pd.DataFrame:
    """Loads CSV file at specified path and delivers a Pandas Dataframe"""
    if not path.exists(path_to_file):
        raise FileNotFoundError("File does not exist.")

    return pd.read_csv(path_to_file, delimiter=';')

def find_last_stock_per_day(df: pd.DataFrame) -> pd.DataFrame:
    """Finds latest stock per day at 'closing time' per day"""
    df = df.sort_values("Date") # Sorting by date and time
    df['Date'] = df['Date'].astype(str).str[:10] # Makes date unique, not time. Later: Exclude last by date.
    df = df.groupby(["Kod", "Date"]).last().reset_index() # Here: Last by date.
    return df

def extract_stock_growth(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts stock growth at 'closing time' per day and creates a new DataFrame
    with aggregate of flat row of data per Kod"""
    last_stocks = find_last_stock_per_day(df)
    last_stocks["Growth"] = last_stocks.groupby(["Kod"])["Kurs"].pct_change()
    merged = last_stocks.groupby("Kod").agg(
        Date_start=('Date', 'first'),
        Kurs_start=('Kurs', 'first'),
        Date_end=('Date', 'last'),
        Kurs_end=('Kurs', 'last'),
        Growth=('Growth', 'last')
    ).reset_index()
    return merged


def pick_winners(df: pd.DataFrame) -> pd.DataFrame:
    """Creates Winner entries"""
    df_sorted = df.sort_values("Growth", ascending=False).reset_index(drop=True)
    df_sorted["rank"] = df_sorted.index + 1
    return df_sorted