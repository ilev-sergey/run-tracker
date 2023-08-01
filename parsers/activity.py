import re
from datetime import date, datetime, timedelta


def get_lap_times(text: str) -> list[timedelta]:
    lap_times = []
    for time, ms in re.findall(r"(\d{2}:\d{2}(\.\d{2,3})?)", text):
        res = time
        if ms == "":
            res += ".0"

        lap_time = datetime.strptime(res, "%M:%S.%f").time()
        lap_times.append(lap_time)
    lap_times = [
        datetime.combine(date.min, lap_time) - datetime.min for lap_time in lap_times
    ]  # convert to timdelta object
    return lap_times


if __name__ == "__main__":
    string = "01:01 02:02.02 03:03.300"
    lap_times = get_lap_times(string)
    print([str(time) for time in lap_times])
