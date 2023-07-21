WITH avg_lap_time AS (
    SELECT start_time,
        time(AVG(strftime('%s', lap_time)), 'unixepoch') || '.' || printf('%03d', AVG(SUBSTR(lap_time, -3))) as avg_lap_time,
        count(lap_time) * 0.4 as distance
    FROM lap_times
    WHERE JULIANDAY(DATETIME('now')) - JULIANDAY(DATETIME(start_time)) < :period
        and user_id = :user_id
    GROUP BY start_time
)
SELECT time(AVG(strftime('%s', avg_lap_time)), 'unixepoch') || '.' || printf('%03d', AVG(SUBSTR(avg_lap_time, -3))) as avg_time,
    avg(distance) as avg_distance
from avg_lap_time