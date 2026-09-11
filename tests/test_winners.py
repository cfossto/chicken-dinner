from pathlib import Path

from fastapi.testclient import TestClient

from chicken_dinner.main import app

FIXTURE_CSV = Path(__file__).parent / "fixtures" / "sample_results.csv"

client = TestClient(app)


def test_root_returns_welcome_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Winner, winner! Chicken Dinner!"}


def test_results_returns_200_ok(monkeypatch):
    monkeypatch.setenv("RESULTS_CSV_PATH", str(FIXTURE_CSV))

    response = client.get("/results")

    assert response.status_code == 200


def test_results_response_is_valid_json_structure(monkeypatch):
    monkeypatch.setenv("RESULTS_CSV_PATH", str(FIXTURE_CSV))

    data = client.get("/results").json()

    assert "winners" in data
    assert isinstance(data["winners"], list)


def test_results_contains_correct_data_types(monkeypatch):
    monkeypatch.setenv("RESULTS_CSV_PATH", str(FIXTURE_CSV))

    winners = client.get("/results").json()["winners"]

    for winner in winners:
        assert isinstance(winner.get("rank"), int)
        assert isinstance(winner.get("name"), str)
        assert isinstance(winner.get("percent"), float)
        assert isinstance(winner.get("latest"), int)


def test_results_exact_data_match(monkeypatch):
    monkeypatch.setenv("RESULTS_CSV_PATH", str(FIXTURE_CSV))

    response = client.get("/results")

    assert response.json() == {
        "winners": [
            {"rank": 1, "name": "NCC", "percent": 30.0, "latest": 65},
            {"rank": 2, "name": "ABB", "percent": 10.0, "latest": 110},
        ]
    }


def test_results_missing_file_returns_500(monkeypatch):
    monkeypatch.setenv("RESULTS_CSV_PATH", str(FIXTURE_CSV.parent / "does-not-exist.csv"))

    response = client.get("/results")

    assert response.status_code == 500
    assert response.json() == {"detail": "Can't locate local stock file. Contact Admin."}
