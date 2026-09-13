"""
I wanted to use Pandas here, since it is the best tool for the job.
Of course, we can do this with the Standardlib as well. But I reasoned
that Pandas was the right choice.

The thing that differs from stdlib is that I would have used the
internal csv package for reading and/or writing. I would probably have
made Pydantic types, dataclasses or pure objects from scratch.

But for this project Pandas is fine.

As you can see, we are keeping the DataFrame format in order to
save bandwidth from having to reformat and transform at every run.
Reasoning was that it is better to transform the CSV to a DataFrame
and let functions manipulate that DataFrame through the whole process.
It is only transformed to its endstate when it needs to have a specific format (like JSON or Dict).
That way - manipulation of data is coherent and transformation only depends
on the desired output.
"""

import pandas as pd
from pathlib import Path


def load_csv(path_to_file: str) -> pd.DataFrame:
    """Loads CSV file at specified path and delivers a Pandas Dataframe"""

    path = Path(path_to_file)
    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path_to_file}")
    try:
        df = pd.read_csv(path_to_file, delimiter=';', on_bad_lines="error")
        return df
    except pd.errors.ParserError:
        raise ValueError(f"CSV is corrupt: {path_to_file}")


def _find_last_stock_per_day(df: pd.DataFrame) -> pd.DataFrame:
    """Finds latest stock per day at 'closing time' per day"""

    df = df.sort_values("Date") # Sorting by date and time
    pd.to_datetime(df['Date'], format="mixed")
    print(df)
    df = df.groupby(["Kod", "Date"]).last().reset_index() # Here: Last by date.
    return df

def _extract_stock_growth(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts stock growth at 'closing time' per day and creates a new DataFrame
    with aggregate of flat row of data per Kod"""

    last_stocks = _find_last_stock_per_day(df)
    last_stocks["Growth"] = (last_stocks.groupby(["Kod"])["Kurs"].pct_change()*100).round(2)
    merged = last_stocks.groupby("Kod").agg(
        Date_start=('Date', 'first'),
        Kurs_start=('Kurs', 'first'),
        Date_end=('Date', 'last'),
        Kurs_end=('Kurs', 'last'),
        Growth=('Growth', 'last')
    ).reset_index()
    return merged

def extract_and_rank_stocks(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts stocks and their growth from a Pandas DataFrame with stocks. Returns sorted and ranked stocks."""
    df = _extract_stock_growth(df)
    df_sorted = df.sort_values("Growth", ascending=False).reset_index(drop=True)
    df_sorted["rank"] = df_sorted.index + 1
    return df_sorted


def pick_winners(df: pd.DataFrame) -> pd.DataFrame:
    """Creates Winner entries and filters out loser stocks."""
    df_sorted = extract_and_rank_stocks(df)
    df_sorted = df_sorted[df_sorted["Growth"] >=0] # Filter out loser stocks

    return df_sorted