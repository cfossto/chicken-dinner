from collections import defaultdict
from pathlib import Path
from typing import List, Dict
import csv


def load_csv(path: Path) -> List[Dict]:
    """Loads cisv and returns as list of dicts"""
    with open(path) as csv_file:
        # I know we lack input validation, but is out of scope of assignment
        reader = csv.DictReader(csv_file, delimiter=";")
        return list(reader)


def _sort_results_by_column(entries: List[Dict], column: str) -> List[Dict]:
    """Sort entries by column. Returns a list of dicts with same payload as input"""
    return sorted(entries, key=lambda k: k[column], reverse=False)


def _extract_last_entry_per_day(entries: List[Dict]) -> List[Dict]:
    """Finds the last event per day and makes an entry."""
    last_day_occurrences = {}

    entries = _sort_results_by_column(entries, "Date")  # Enforce sorting

    for entry in entries:
        date = entry["Date"][:10]
        code = entry["Kod"]
        combine_key = (date, code)  # Creates a lookup on this tuple. Overwrites "earlier" posts.
        last_day_occurrences[combine_key] = entry  # Add to occurrence dict

    return list(last_day_occurrences.values())


def _growth_in_percent(start: int, end: int) -> float:
    """Returns growth in percent as a float with 2 decimal places."""
    if start == 0:
        raise ValueError("start cannot be 0")
    growth = (end - start) / start * 100
    return round(growth, 2)


def _compile_pairs(entries: List[Dict]) -> List[List[Dict]]:
    """Compiles pairs of entries into a list of dicts with same payload as input based on 'Kod'"""
    # Rearrange in pairs by date
    sorted_entries = _sort_results_by_column(entries, "Date")
    grouped_data = defaultdict(list)
    for entry in sorted_entries:
        grouped_data[entry["Kod"]].append(entry)

    return list(grouped_data.values())


def _rank_growth(entries: List[List[Dict]]) -> List[Dict]:
    """Rank growth in percent from coupled entries based on posts per end of day."""

    winner_list = []  # We are delivering the final collection in this list.

    # Handle both start and end entries in the groupings.
    for entry in entries:
        winners = {}
        growth = _growth_in_percent(int(entry[0]["Kurs"]), int(entry[1]["Kurs"]))
        if growth > 0.0:
            winners["percent"] = growth
            winners["name"] = entry[0].get("Kod")
            winners["latest"] = entry[1].get("Kurs")  # Get the Kurs from the latest entry
            winner_list.append(winners)
    winner_list = sorted(winner_list, key=lambda k: k["percent"], reverse=True)
    for i in range(0, len(winner_list)):
        winner_list[i]["rank"] = i + 1
    return winner_list


def compile_result(entries: List[Dict]) -> List[Dict]:
    """This is the main function we call to compile the final winners."""
    sorted_entries = _sort_results_by_column(entries, "Date")
    extracted_last_day = _extract_last_entry_per_day(sorted_entries)
    extracted_pairs = _compile_pairs(extracted_last_day)
    final_result = _rank_growth(extracted_pairs)
    return final_result


"""
if __name__ == "__main__":
    from pprint import pprint
    c = load_csv(Path(__file__).parent.parent.parent.parent / "results.csv")

    compiled_result = compile_result(c)
    pprint(compiled_result)
"""
