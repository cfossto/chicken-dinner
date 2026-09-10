# Winner, Winner, Chicken dinner!

This repo is a sample repo where the end goal is to serve
arbitrary "stock exchange" winners from a pre-generated CSV file.
Result will be delvered in a structured CSV.

This project utilize:

- UV
- FastAPI
- Pandas for file handling/parsing
- Pydantic for validation
- Bonus: raw http client for base lib showoff
- Bonus: raw validation examples for base lib showoff


# Important note
While this application mainly use FastAPI for the web layer,
I am providing an example of how to create an endpoint with
a more barebone entrypoint with Python HTTP.

Also:
No AI prompting has been used in creating this project.
While LLMs are a part of a modern dev stack, this is more for showcase
about my current Python level and my understanding of the language.