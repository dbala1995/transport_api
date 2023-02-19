from sqlalchemy.orm import Session

from . import models, schemas


def get_times_checked_by_id(db: Session, transport_id: int):
    return (
        db.query(models.TimesChecked)
        .filter(models.TimesChecked.id == transport_id)
        .first()
    )


def get_times_checked_by_origin_station(
    db: Session,
    origin_station: str,
    destination_station: str = None,
    date_of_travel: str = None,
    time_of_departure: str = None,
):
    query_ret = db.query(models.TimesChecked).filter(
        models.TimesChecked.start_destination == origin_station
    )
    if destination_station:
        query_ret.filter(models.TimesChecked.end_destination == destination_station)
    if time_of_departure:
        query_ret.filter(
            models.TimesChecked.time_of_departure_at_start >= time_of_departure
        )
    if date_of_travel:
        query_ret.filter(models.TimesChecked.date_of_travel == date_of_travel)

    return query_ret


def get_times_checked(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TimesChecked).offset(skip).limit(limit).all()


def create_times_checked(db: Session, times_checked: schemas.TimesCheckedCreate):
    db_time_checked = models.TimesChecked(**times_checked.dict())
    db.add(db_time_checked)
    db.commit()
    db.refresh(db_time_checked)
    return db_time_checked
