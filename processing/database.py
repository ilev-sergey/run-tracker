import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("users_data.db")
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
