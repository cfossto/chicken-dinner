from pathlib import Path

import pytest

from chicken_dinner.bonus.stdlibdatautils import (
    _compile_pairs,
    _extract_last_entry_per_day,
    _growth_in_percent,
    _rank_growth,
    _sort_results_by_column,
    compile_result,
    load_csv,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _make_rows(rows):
    return [{"Date": date, "Kod": kod, "Kurs": str(kurs)} for date, kod, kurs in rows]


# Mirrors SAMPLE_ROWS in test_datautils.py: two closing prices per stock, one
# per day. A falls, B and C rise, with B rising the most.
SAMPLE_ROWS = _make_rows(
    [
        ("2024-01-01 09:00:00", "A", 100),
        ("2024-01-02 09:00:00", "A", 90),
        ("2024-01-01 09:00:00", "B", 50),
        ("2024-01-02 09:00:00", "B", 75),
        ("2024-01-01 09:00:00", "C", 200),
        ("2024-01-02 09:00:00", "C", 202),
    ]
)


def test_load_csv_returns_list_of_dicts_with_expected_keys():
    rows = load_csv(FIXTURES / "sample_results.csv")

    assert list(rows[0].keys()) == ["Date", "Kod", "Kurs"]
    assert len(rows) == 4


def test_load_csv_missing_file_raises_file_not_found_error():
    with pytest.raises(FileNotFoundError):
        load_csv(FIXTURES / "does-not-exist.csv")


def test_sort_results_by_column_sorts_ascending():
    unsorted_rows = [SAMPLE_ROWS[1], SAMPLE_ROWS[0], SAMPLE_ROWS[3], SAMPLE_ROWS[2]]

    sorted_rows = _sort_results_by_column(unsorted_rows, "Date")

    assert [row["Date"] for row in sorted_rows] == sorted(row["Date"] for row in unsorted_rows)


def test_extract_last_entry_per_day_keeps_latest_entry_per_day_and_code():
    rows = _make_rows(
        [
            ("2024-01-01 09:00:00", "A", 100),
            ("2024-01-01 17:00:00", "A", 105),  # later same-day entry should win
            ("2024-01-02 09:00:00", "A", 110),
        ]
    )

    result = _sort_results_by_column(_extract_last_entry_per_day(rows), "Date")

    assert [row["Kurs"] for row in result] == ["105", "110"]


def test_growth_in_percent_calculates_correctly():
    assert _growth_in_percent(50, 75) == 50.0
    assert _growth_in_percent(200, 202) == 1.0
    assert _growth_in_percent(100, 90) == -10.0


def test_growth_in_percent_raises_on_zero_start():
    with pytest.raises(ValueError):
        _growth_in_percent(0, 100)


def test_compile_pairs_groups_by_kod():
    pairs = _compile_pairs(SAMPLE_ROWS)

    grouped_by_kod = {group[0]["Kod"]: [row["Kurs"] for row in group] for group in pairs}
    assert grouped_by_kod == {"A": ["100", "90"], "B": ["50", "75"], "C": ["200", "202"]}


def test_rank_growth_orders_by_percent_descending():
    winners = _rank_growth(_compile_pairs(SAMPLE_ROWS))

    assert [w["name"] for w in winners] == ["B", "C"]
    assert [w["rank"] for w in winners] == [1, 2]


def test_rank_growth_filters_out_zero_and_negative_growth():
    pairs = _compile_pairs(
        _make_rows(
            [
                ("2024-01-01 09:00:00", "FLAT", 100),
                ("2024-01-02 09:00:00", "FLAT", 100),
                ("2024-01-01 09:00:00", "DOWN", 100),
                ("2024-01-02 09:00:00", "DOWN", 90),
            ]
        )
    )

    assert _rank_growth(pairs) == []


# compile_result mirrors extract_and_rank_stocks / pick_winners from the
# Pandas solution: same growth percentages, same ranks, same winners.


def test_compile_result_orders_by_growth_descending():
    winners = compile_result(SAMPLE_ROWS)

    assert [w["name"] for w in winners] == ["B", "C"]
    assert [w["rank"] for w in winners] == [1, 2]


def test_compile_result_computes_percent_growth():
    winners = {w["name"]: w for w in compile_result(SAMPLE_ROWS)}

    assert winners["B"]["percent"] == 50.0
    assert winners["C"]["percent"] == 1.0


def test_compile_result_filters_out_negative_growth():
    names = [w["name"] for w in compile_result(SAMPLE_ROWS)]

    assert "A" not in names


def test_compile_result_matches_fixture_exact_data():
    rows = load_csv(FIXTURES / "sample_results.csv")

    assert compile_result(rows) == [
        {"percent": 30.0, "name": "NCC", "latest": "65", "rank": 1},
        {"percent": 10.0, "name": "ABB", "latest": "110", "rank": 2},
    ]
