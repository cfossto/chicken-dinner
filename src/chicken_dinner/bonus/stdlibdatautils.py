from pathlib import Path
from stdlibdatamodels import WinnerEntries, RawData
from typing import List, Dict
import csv

def load_csv(path: Path) -> List[Dict]:
    """Loads cisv and returns as list of dicts"""
    reader = csv.DictReader(open(path), delimiter=";")
    return list(reader)

def sort_results_by_column(entries: List[Dict], column: str) -> List[Dict]:
    """Sort entries by column. Returns a list of dicts with same payload as input"""
    return sorted(entries, key=lambda k: k[column], reverse=False)


def extract_last_entry_per_day(entries: List[Dict]) -> List[Dict]:
    slut_kurser = []


def _growth_in_percent(start: int, end: int) -> float:
    """Returns growth in percent as a float with 2 decimal places."""
    growth = ((end-start)/start) * 100
    if growth <= 0:
        growth = -growth
    return round(growth,2)

def rank_and_compile(entries: List[Dict]) -> List[Dict]:
    pass


c = load_csv(Path(__file__).parent.parent.parent.parent / "results.csv")

sorted_entries = sort_results_by_column(c, "Date")

d = int(sorted_entries[0]['Kurs'])
m = int(sorted_entries[2]['Kurs'])

print(d)
print(m)

gr = growth_in_percent(m,d)
print(gr)