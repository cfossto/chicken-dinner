from pydantic import BaseModel


class WinnersEntries(BaseModel):
    rank: int
    name: str
    percent: float
    latest: int
