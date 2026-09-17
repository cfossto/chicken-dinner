from dataclasses import dataclass
from datetime import datetime
from typing import List

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