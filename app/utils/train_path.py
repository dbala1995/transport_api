from pydantic import BaseModel

from app.utils.train_time import TrainTime


class TrainPath(BaseModel):
    from_station: str
    to_station: str
    departure_time: TrainTime
    arrival_time: TrainTime
