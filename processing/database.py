import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Union


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect("users_data.db")
conn.row_factory = dict_factory
cur = conn.cursor()
with conn:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS lap_times (
            user_id INT,
            start_time TEXT,
            lap_time TEXT
        )
        """
    )


async def add_user_data(user_id: int, start_time: datetime, lap_times: list[timedelta]):
    records = [
        [user_id, start_time, "0" + str(lap_time)[:-3]] for lap_time in lap_times
    ]  # HH:MM:SS.fff
    with conn:
        cur.executemany(
            "INSERT INTO lap_times VALUES (?, ?, ?)",
            records,
        )


async def avg_for_period(
    user_id: int, period_in_days: int = 10_000
) -> Optional[dict[str, Union[str, float]]]:
    with conn, open("processing/queries/avg_for_period.sql") as query_file:
        result = cur.execute(
            query_file.read(), {"user_id": user_id, "period": period_in_days}
        ).fetchone()
        if all(result.values()):
            return result
