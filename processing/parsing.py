from datetime import datetime, date, timedelta
import re
from dateutil.parser import parse


def get_timestamp(message: str) -> datetime:
    date = parse(message.splitlines()[1])  # parse line with date
    return date


def get_lap_times(message: str) -> list[timedelta]:
    lap_times = [
        datetime.strptime(lap_time, "%M:%S.%f").time()  # convert to time object
        for lap_time in re.findall("\+([^ ]*)", message)  # find all lap_times
    ]
    lap_times = [
        datetime.combine(date.min, lap_time) - datetime.min for lap_time in lap_times
    ]  # convert to timdelta object
    return lap_times
