import pandas as pd

def load_csv(path_to_file: str) -> pd.DataFrame:
    """Loads CSV file at specified path and delivers a Pandas Dataframe"""
    df = pd.read_csv(path_to_file, delimiter=';')
    return df

def find_max_last_stock(df: pd.DataFrame) -> pd.DataFrame:
    """Finds latest stock per day at 'closing time' per day"""
    df.sort_values("date") # Sorting by date and time
    df['Date'] = df['Date'].astype(str).str[:10] # Makes date unique, not time. Later: Exclude last by date.
    df.groupby(["Kod", "Date"])["Kurs"].last().reset_index() # Here: Last by date.
    return df

