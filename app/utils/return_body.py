from typing import List
from pydantic import BaseModel

from app.utils.train_path import TrainPath


class ReturnBody(BaseModel):
    success: bool
    message: str
    time_of_arrival: str
    journey: List[TrainPath]
