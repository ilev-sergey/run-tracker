import re
from datetime import date, datetime
from typing import Any, Optional

from aiogram.filters import BaseFilter
from aiogram.types import Message


class isStopwatchMessage(BaseFilter):
    async def __call__(self, message: Message) -> Optional[dict[str, Any]]:
        if not message.text.startswith("Stopwatch"):
            return
        try:
            start_time = datetime.strptime(
                message.text.splitlines()[1],
                "%B %d, %Y %I:%M %p ",
            )
            lap_times = re.findall(
                r"\+([0-9][0-9]\:[0-9][0-9]\.[0-9][0-9])",
                message.text,
            )
            lap_times = [
                datetime.combine(
                    date.min, datetime.strptime(lap_time, "%M:%S.%f").time()
                )
                - datetime.min
                for lap_time in lap_times
            ]
        except:
            return
        else:
            return {"start_time": start_time, "lap_times": lap_times}
