from collections import defaultdict
from pathlib import Path
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
    growth = (end - start) / start * 100
    return round(growth,2)

def compile_pairs(entries: List[Dict]) -> List[List[Dict]]:
    # Rearrange in pairs by date
    sorted_entries = sort_results_by_column(entries, "Date")
    grouped_data = defaultdict(list)
    for entry in sorted_entries:
        grouped_data[entry["Kod"]].append(entry)

    return list(grouped_data.values())

def rank_growth(entries: List[List[Dict]]) -> List[Dict]:
    """Rank growth in percent from coupled entries based on posts per end of day."""

    winner_list = [] # We are delivering the final collection in this list.

    # Handle both start and end entries in the groupings.
    for entry in entries:
        winners = {}
        growth = _growth_in_percent(int(entry[0]['Kurs']), int(entry[1]['Kurs']))
        if growth > 0.0:
            winners['percent'] = growth
            winners['name'] = entry[0].get("Kod")
            winners['latest'] = entry[1].get("Kurs") # Get the Kurs from the latest entry
            winner_list.append(winners)
    winner_list = sorted(winner_list, key=lambda k: k['percent'], reverse=True)
    return winner_list