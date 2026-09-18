from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict


@dataclass
class WinnerEntries:
    rank: int
    name: str
    percent: float
    latest: int


@dataclass
class WinnerList:
    winners: List[WinnerEntries]


@dataclass
class RawData:
    Date: datetime
    Kod: str
    Kurs: float


@dataclass
class FlattenedWinners:
    first: datetime
    last: datetime
    first_top: int
    latest_top: int


@dataclass
class WinnerPairs:
    pairs: List[List[Dict]]
