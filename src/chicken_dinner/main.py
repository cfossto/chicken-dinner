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

app = FastAPI()

# Define middlewares + CORS
CORS = {}

# Main entrypoint

@app.get("/")
async def root_get():
    return { "message": "" }

@app.get("/results")
async def get_all_results():
    '''Returns sorted stocks in descending order'''
    pass


@app.get("/results/{id}")
async def get_specific_result(id):
    pass