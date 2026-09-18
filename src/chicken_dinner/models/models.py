from pydantic import BaseModel
from typing import List

__all__ = ["WinnerCollection", "WinnerEntries"]


class WinnerEntries(BaseModel):
    rank: int
    name: str
    percent: float
    latest: int


class WinnerCollection(BaseModel):
    winners: List[WinnerEntries]
