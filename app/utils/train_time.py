from pydantic import BaseModel, validator
from fastapi import HTTPException
from datetime import time


class TrainTime(BaseModel):
    time: str

    @validator("time")
    def time_must_be_5_chars_long(cls, v):
        if len(v) < 5:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": "time does not contain 5 characters",
                },
            )
        if ":" not in v:
            raise HTTPException(
                status_code=400,
                detail={"success": False, "message": "time does not contain ':'"},
            )
        if v[2] != ":":
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": "':' not in correct location, please ensure it is third character of time",
                },
            )
        return v

    def get_hour(self):
        return int(self.time[:2])

    def get_minute(self):
        return int(self.time[3:])

    def get_time_as_time(self):
        return time(hour=self.get_hour(), minute=self.get_minute())

    def get_total_minutes(self):
        minutes = (self.get_hour() * 60) + self.get_minute()
        return minutes
