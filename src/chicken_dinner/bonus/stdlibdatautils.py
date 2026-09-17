from pathlib import Path
from typing import List, Dict
import csv
from pprint import pprint

def load_csv(path: Path) -> List[Dict]:
    """Loads cisv and returns as list of dicts"""
    reader = csv.DictReader(open(path), delimiter=";")
    return list(reader)

def sort_results_by_column(entries: List[Dict], column: str) -> List[Dict]:
    """Sort entries by column. Returns a list of dicts with same payload as input"""
    return sorted(entries, key=lambda k: k[column], reverse=False)


def extract_last_entry_per_day(entries: List[Dict]) -> List[Dict]:
    """"""
    last_day_occurrences = {}

    entries = sort_results_by_column(entries, "Date") # Enforce sorting

    for entry in entries:
        date = entry['Date'][:10]
        code = entry['Kod']
        combine_key = (date, code) # Creates a lookup on this tuple. Overwrites "earlier" posts.
        last_day_occurrences[combine_key] = entry # Add to occurrence dict

    return list(last_day_occurrences.values())


def _growth_in_percent(start: int, end: int) -> float:
    """Returns growth in percent as a float with 2 decimal places."""
    if start == 0:
        raise ValueError("start cannot be 0")
    growth = ((end-start)/start) * 100
    return round(abs(growth),2)

def compile_pairs(entries: List[Dict]) -> List[Dict]:
    # Rearrange in pairs after date
    sorted_entries = sort_results_by_column(entries, "Date")
    keys = set([k['Kod'] for k in sorted_entries])
    rearranged_entries = [] # What will be returned

    current_pairs = [] # Compilation of pairs

    # One pass through keys and then compare to sorted entries
    # Append to temporary list before final compilation
    for k in keys:
        for entry in sorted_entries:
            if entry['Kod'] == k:
                current_pairs.append(entry)
        rearranged_entries.append(current_pairs)
        current_pairs = []
    return rearranged_entries

def rank_growth(entries: List[List[Dict]]) -> List[Dict]:
    pass


c = load_csv(Path(__file__).parent.parent.parent.parent / "results.csv")

b = extract_last_entry_per_day(c)
h = compile_pairs(b)

pprint(h)