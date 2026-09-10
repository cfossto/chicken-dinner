from fastapi import FastAPI
from fastapi.testclient import TestClient

# Replace this import with your actual FastAPI app instance
# from your_main_file import app

app = FastAPI()


# Dummy endpoint replicating your expected output for the test to run
@app.get("/winners")
def get_winners():
    return {
        "winners": [
            {"rank": 1, "name": "AddLife B", "percent": 40.74, "latest": 38},
            {"rank": 2, "name": "NCC", "percent": 1.68, "latest": 121},
            {"rank": 3, "name": "ABB", "percent": 1.37, "latest": 222}
        ]
    }


client = TestClient(app)


def test_endpoint_returns_200_ok():
    response = client.get("/winners")
    assert response.status_code == 200


def test_response_is_valid_json_structure():
    response = client.get("/winners")
    data = response.json()

    assert "winners" in data
    assert isinstance(data["winners"], list)


def test_response_contains_correct_data_types():
    response = client.get("/winners")
    winners = response.json()["winners"]

    for winner in winners:
        assert isinstance(winner.get("rank"), int)
        assert isinstance(winner.get("name"), str)
        assert isinstance(winner.get("percent"), float)
        assert isinstance(winner.get("latest"), int)


def test_exact_data_match():
    response = client.get("/winners")
    expected_output = {
        "winners": [
            {"rank": 1, "name": "AddLife B", "percent": 40.74, "latest": 38},
            {"rank": 2, "name": "NCC", "percent": 1.68, "latest": 121},
            {"rank": 3, "name": "ABB", "percent": 1.37, "latest": 222}
        ]
    }
    assert response.json() == expected_output