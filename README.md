# Winner, Winner, Chicken dinner!

<img width="2816" height="1536" alt="chickendinner" src="https://github.com/user-attachments/assets/f9f51da3-efdb-4515-8fbb-e9a8862e1c74" />


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
No AI coding has been used in creating this project. I have used Gemini
and Google for looking up documentation of Pandas and edge cases to solve
correctly for how I wanted to extract the winner data.

While LLMs are a part of a modern dev stack, this is more for showcase
about my current Python level and my understanding of the language.
I did, however, use LLMs for generating test cases in order to save time.
But the rest of the code stems from my own Python experience.
