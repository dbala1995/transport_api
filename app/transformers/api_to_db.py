from typing import Dict
from datetime import date

from app.sqlite.schemas import TimesChecked


class APIToDB:
    def __init__(self) -> None:
        pass

    def convert_departure_to_db(
        self, origin_station: str, date_of_travel: date, departure: Dict
    ) -> TimesChecked:
        """
        Function will convert departure dict and convert into TimesChecked object ready to be posted into DB
        """
        times_checked = TimesChecked(
            start_destination=origin_station,
            end_destination=departure["station_detail"]["calling_at"][0][
                "station_code"
            ],
            date_of_travel=str(date_of_travel),
            time_of_arrival_at_end=self._join_date_and_time(
                date_of_travel=date_of_travel,
                time=departure["station_detail"]["calling_at"][0]["aimed_arrival_time"],
            ),
            time_of_departure_at_start=self._join_date_and_time(
                date_of_travel=date_of_travel, time=departure["aimed_departure_time"]
            ),
        )

        return times_checked

    def get_time(self, date_time: str) -> str:
        """
        Function will return time from datetime string in db to be used in rest of application
        """
        date_ret, time_ret = self._split_date_and_time(date_time=date_time)
        return time_ret

    def _join_date_and_time(self, date_of_travel: date, time: str) -> str:
        """
        Function will join date and time ready to be posted into DB
        """
        return f"{str(date_of_travel)} {time}"

    def _split_date_and_time(self, date_time: str) -> date and str:
        """
        Function will convert date_time from db to be used as seperate time and date in app
        """
        return (
            date(
                year=int(date_time[:4]),
                month=int(date_time[5:7]),
                day=int(date_time[8:10]),
            ),
            date_time[-5:],
        )
