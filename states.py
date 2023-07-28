from aiogram.fsm.state import StatesGroup, State


class UTC_Offset(StatesGroup):
    choosing_timezone = State()


class Activity(StatesGroup):
    entering_date = State()
    entering_time = State()
    entering_lap_times = State()
    confirming_result = State()
