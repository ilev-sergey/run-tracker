import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("users_data.db")
cur = conn.cursor()
with conn:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS lap_times (
            user_id INT,
            timestamp TEXT,
            lap_time TEXT
        )
        """
    )


async def add_user_data(user_id: int, timestamp: datetime, lap_times: list[timedelta]):
    records = [[user_id, timestamp, str(lap_time)] for lap_time in lap_times]
    with conn:
        cur.executemany(
            f"INSERT INTO lap_times VALUES (?, ?, ?)",
            records,
        )
