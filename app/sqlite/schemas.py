from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TimesCheckedBase(BaseModel):
    start_destination: str
    end_destination: str
    date_of_travel: str
    time_of_arrival_at_end: str
    time_of_departure_at_start: str


class TimesCheckedCreate(TimesCheckedBase):
    pass


class TimesChecked(TimesCheckedBase):
    id: Optional[int]

    class Config:
        orm_mode = True
