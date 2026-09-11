"""
While this application mainly use FastAPI for the web layer,
I am providing an example of how to create an endpoint with
a more barebone entrypoint with Python HTTP.

Also:
No AI prompting has been used in creating this project.
While LLMs are a part of a modern dev stack, this is more for showcase
about my current Python level and my understanding of the language.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from .models.models import WinnerCollection
from .datautils.datautils import pick_winners, load_csv

app = FastAPI()

# Define allowed origins and methods
origins = ["http://localhost:8000","http://localhost"]
methods = ["GET"]

# Define middlewares + CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=methods,
)

# Main entrypoint

@app.get("/")
async def root_get():
    """We just return a simple response on the Root. Better to have semantics involved from start."""
    return { "message": "Winner, winner! Chicken Dinner!" }

@app.get("/results")
async def get_results():
    try:
        df = load_csv("../../results.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Can't locate local stock file. Contact Admin.")
    except ValueError:
        raise HTTPException(status_code=500, detail="Corrupt CSV file.")

    df_winners = pick_winners(df)
    df_formatted = df_winners.rename(columns={
        "Kod": "name",
        "Growth": "percent",
        "Kurs_end": "latest"
    })

    winners_list = df_formatted.to_dict(orient="records")
    return WinnerCollection(winners=winners_list)