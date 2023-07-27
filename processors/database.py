import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Union, Any


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


async def run_query(query: str, data: dict[Any, Any]) -> Optional[dict]:
    if query.endswith(".sql"):  # if query is .sql file, read query
        with open(f"processors/queries/{query}") as query_file:
            query = query_file.read()
    with conn:
        result = cur.execute(query, data).fetchone()
    if isinstance(result, dict) and all(result.values()) is not None:
        return result


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
    return await run_query(
        query="avg_for_period.sql",
        data={"user_id": user_id, "period": period_in_days},
    )
