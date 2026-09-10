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
        raise FileNotFoundError()

    return pd.read_csv(path_to_file, delimiter=';')

def find_last_stock_per_day(df: pd.DataFrame) -> pd.DataFrame:
    """Finds latest stock per day at 'closing time' per day"""
    df.sort_values("Date") # Sorting by date and time
    df['Date'] = df['Date'].astype(str).str[:10] # Makes date unique, not time. Later: Exclude last by date.
    df = df.groupby(["Kod", "Date"]).last().reset_index() # Here: Last by date.
    return df

def find_winners(df: pd.DataFrame) -> pd.DataFrame:
    """Finds winners based on stock performance between days"""
    pass