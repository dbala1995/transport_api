from sqlalchemy import Column, Integer, String

from .database import Base


class TimesChecked(Base):
    __tablename__ = "times_checked"

    id = Column(Integer, primary_key=True, index=True)
    start_destination = Column(String)
    end_destination = Column(String)
    date_of_travel = Column(String)
    time_of_arrival_at_end = Column(String)
    time_of_departure_at_start = Column(String)
