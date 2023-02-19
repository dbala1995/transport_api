from typing import List
import requests
import os
from datetime import date, time, datetime
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Query, HTTPException
from app.transformers.api_to_db import APIToDB
from app.utils.return_body import ReturnBody
from app.utils.train_path import TrainPath
from app.sqlite.schemas import TimesChecked
from app.sqlite.crud import (
    get_times_checked,
    get_times_checked_by_id,
    create_times_checked,
    get_times_checked_by_origin_station,
)
from app.sqlite.database import SessionLocal, Base, engine
from app.utils.train_time import TrainTime


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app_id = os.getenv("APP_ID")
app_key = os.getenv("APP_KEY")
transport_domain = os.getenv("TRANSPORT_DOMAIN", "https://transportapi.com")

app = FastAPI()

api_to_db = APIToDB()


@app.get("/")
def read_root():
    return {"Test": "Success"}


@app.get("/destination-time", response_model=ReturnBody)
async def obtain_time(
    db: Session = Depends(get_db),
    start_date: date = Query(
        None,
        description="Date which to start searching your journey.",
        example="2023-02-10",
    ),
    start_time: str = Query(
        None, description="Time which to start searching for journey.", example="14:17"
    ),
    max_wait_time: int = Query(
        None,
        description="The maximum wait time, in minutes, a traveller is willing to wait for a connection. Defaults to 60 minutes.",
        example="60",
    ),
    route: List[str] = Query(
        ...,
        description="A list containing a the train stations, in CRS format, which traveller wishes to use for their journey, minimum length of two.",
        example=["LBG", "SAJ", "NWX", "BXY"],
    ),
):
    if not start_date:
        start_date = date.isoformat(datetime.now().date())

    if not start_time:
        start_time = time.isoformat(datetime.now().time())[:5]
    else:
        check_start_time = TrainTime(time=start_time)

    if not max_wait_time:
        max_wait_time = 60

    if len(route) < 2:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "message": "Number of train stations provided is less than 2, not possible to calculate destination time. Please provide at least two train stations.",
            },
        )

    journey: List[TrainPath] = []
    for i, train_station in enumerate(route):
        if i + 1 < len(route):
            check_saved_departures: List[
                TimesChecked
            ] = get_times_checked_by_origin_station(
                db=db,
                origin_station=train_station,
                date_of_travel=start_date,
                destination_station=route[i + 1],
                time_of_departure=start_time,
            )
            if type(check_saved_departures) == list:
                arrival_time = TrainTime(
                    time=api_to_db.get_time(
                        check_saved_departures[0].time_of_arrival_at_end
                    )
                )
                departure_time = TrainTime(
                    time=api_to_db.get_time(
                        check_saved_departures[0].time_of_departure_at_start
                    )
                )
                path = TrainPath(
                    from_station=train_station,
                    to_station=route[i + 1],
                    departure_time=departure_time,
                    arrival_time=arrival_time,
                )
                journey.append(path)
                continue
            res = requests.get(
                f"{transport_domain}/v3/uk/train/station/{train_station}/{start_date}/{start_time}/timetable.json?app_id={app_id}&app_key={app_key}&calling_at={route[i+1]}&train_status=passenger&station_detail=calling_at"
            )
            if res.status_code == 200:
                if res.json()["departures"]["all"]:
                    for departure in res.json()["departures"]["all"]:
                        times_checked = api_to_db.convert_departure_to_db(
                            origin_station=train_station,
                            date_of_travel=start_date,
                            departure=departure,
                        )
                        create_times_checked(db=db, times_checked=times_checked)

                        arrival_time = TrainTime(
                            time=departure["station_detail"]["calling_at"][0][
                                "aimed_arrival_time"
                            ]
                        )
                        departure_time = TrainTime(
                            time=departure["aimed_departure_time"]
                        )
                        path = TrainPath(
                            from_station=train_station,
                            to_station=route[i + 1],
                            departure_time=departure_time,
                            arrival_time=arrival_time,
                        )
                        if i > 0:
                            time_waiting: int = (
                                departure_time.get_total_minutes()
                                - journey[-1].arrival_time.get_total_minutes()
                            )

                            if time_waiting > max_wait_time:
                                raise HTTPException(
                                    status_code=400,
                                    detail={
                                        "success": False,
                                        "message": "Wait time exceeded max_wait_time limit set during request.",
                                        "departing_station": train_station,
                                        "arrival_station": route[i + 1],
                                        "wait_time": time_waiting,
                                    },
                                )

                        start_time = departure["station_detail"]["calling_at"][0][
                            "aimed_arrival_time"
                        ]
                        journey.append(path)
                        break
                else:
                    raise HTTPException(
                        status_code=404,
                        detail={
                            "success": False,
                            "message": "Could not find a route for journey",
                            "api_response": res.json(),
                        },
                    )
            else:
                raise HTTPException(status_code=res.status_code, detail=res.json())

    return ReturnBody(
        success=True,
        message=f"Successfully managed to find journey and time of arrival.",
        time_of_arrival=journey[-1].arrival_time.time,
        journey=journey,
    )
