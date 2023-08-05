import re
from datetime import date, datetime
from typing import Any, Optional

from aiogram.filters import BaseFilter
from aiogram.types import Message


class isLapTimesMessage(BaseFilter):
    async def __call__(self, message: Message) -> Optional[dict[str, Any]]:
        try:
            lap_times = []
            for match in re.finditer(
                r"\d{2}:\d{2}\.(\d{2,3})|\d{2}:\d{2}", message.text
            ):
                if match.group(1):
                    datetime_obj = datetime.strptime(match.group(), "%M:%S.%f")
                else:
                    datetime_obj = datetime.strptime(match.group(), "%M:%S")
                lap_time = (
                    datetime.combine(date.min, datetime_obj.time()) - datetime.min
                )
                lap_times.append(lap_time)
            if lap_times:
                return {"lap_times": lap_times}
        except:
            return
