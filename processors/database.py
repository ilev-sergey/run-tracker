import sqlite3
from datetime import datetime, timedelta
from typing import Any, Optional, Union


def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict[str, Any]:
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


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
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_timezones (
            user_id INT PRIMARY KEY,
            timezone INT
        )
        """
    )


async def run_query(query: str, data: dict[Any, Any]) -> Optional[dict]:
    if query.endswith(".sql"):  # if query is .sql file, read query
        with open(f"processors/queries/{query}") as query_file:
            query = query_file.read()
    with conn:
        result = cur.execute(query, data).fetchone()
    if isinstance(result, dict) and all(result.values()):
        return result


async def set_user_timezone(user_id: int, timezone: int) -> None:
    db_timezone = await get_user_timezone(user_id)
    if db_timezone == timezone:
        return
    hours_delta = -timezone if db_timezone is None else -(timezone - db_timezone)
    await update_start_time(user_id=user_id, hours_delta=hours_delta)
    await run_query(
        query="INSERT OR REPLACE INTO user_timezones VALUES(:user_id, :timezone)",
        data={"user_id": user_id, "timezone": timezone},
    )


async def get_user_timezone(user_id: int) -> Optional[int]:
    result = await run_query(
        query="SELECT timezone FROM user_timezones WHERE user_id = :user_id",
        data={"user_id": user_id},
    )

    return result["timezone"] if result else None


async def add_user_data(user_id: int, start_time: datetime, lap_times: list[timedelta]):
    timezone = await get_user_timezone(user_id)
    if timezone:  # if timezone was defined by user
        start_time -= timedelta(hours=timezone)  # convert to UTC

    records = [
        [
            user_id,
            start_time,
            "0"
            + str(lap_time).split(".")[0]
            + f"{lap_time.microseconds/10**6:.3f}"[1:],
        ]
        for lap_time in lap_times
    ]  # HH:MM:SS.fff
    with conn:
        cur.executemany(
            "INSERT INTO lap_times VALUES (?, ?, ?)",
            records,
        )


async def avg_for_period(
    user_id: int, period_in_days: int = 10_000
) -> Optional[dict[str, Union[str, float]]]:
    return await run_query(
        query="avg_for_period.sql",
        data={"user_id": user_id, "period": period_in_days},
    )


async def update_start_time(user_id: int, hours_delta: int) -> None:
    await run_query(
        query="UPDATE lap_times SET start_time=DATETIME(start_time, :hours_delta || ' hours')",
        data={"user_id": user_id, "hours_delta": hours_delta},
    )
