from pathlib import Path

import pandas as pd
import pytest

from chicken_dinner.datautils.datautils import extract_and_rank_stocks, load_csv, pick_winners

FIXTURES = Path(__file__).parent / "fixtures"


def _make_df(rows):
    return pd.DataFrame(rows, columns=["Date", "Kod", "Kurs"])


# Two closing prices per stock, one per day: A falls, B and C rise, with B
# rising the most.
SAMPLE_ROWS = [
    ("2024-01-01 09:00:00", "A", 100),
    ("2024-01-02 09:00:00", "A", 90),
    ("2024-01-01 09:00:00", "B", 50),
    ("2024-01-02 09:00:00", "B", 75),
    ("2024-01-01 09:00:00", "C", 200),
    ("2024-01-02 09:00:00", "C", 202),
]


def test_load_csv_returns_dataframe_with_expected_columns():
    df = load_csv(str(FIXTURES / "sample_results.csv"))

    assert list(df.columns) == ["Date", "Kod", "Kurs"]
    assert len(df) == 4


def test_load_csv_missing_file_raises_file_not_found_error():
    with pytest.raises(FileNotFoundError):
        load_csv(str(FIXTURES / "does-not-exist.csv"))


def test_load_csv_corrupt_file_raises_value_error():
    with pytest.raises(ValueError):
        load_csv(str(FIXTURES / "corrupt_results.csv"))


def test_extract_and_rank_stocks_orders_by_growth_descending():
    df = extract_and_rank_stocks(_make_df(SAMPLE_ROWS))

    assert list(df["Kod"]) == ["B", "C", "A"]
    assert list(df["rank"]) == [1, 2, 3]


def test_extract_and_rank_stocks_computes_percent_growth():
    df = extract_and_rank_stocks(_make_df(SAMPLE_ROWS)).set_index("Kod")

    assert df.loc["B", "Growth"] == 50.0
    assert df.loc["C", "Growth"] == 1.0
    assert df.loc["A", "Growth"] == -10.0


def test_pick_winners_filters_out_negative_growth():
    df = pick_winners(_make_df(SAMPLE_ROWS))

    assert list(df["Kod"]) == ["B", "C"]
    assert (df["Growth"] >= 0).all()


def test_pick_winners_preserves_rank_from_full_ranking():
    df = pick_winners(_make_df(SAMPLE_ROWS)).set_index("Kod")

    # B and C keep the ranks (1 and 2) they earned among all stocks, not a
    # re-numbering of just the winners.
    assert df.loc["B", "rank"] == 1
    assert df.loc["C", "rank"] == 2
