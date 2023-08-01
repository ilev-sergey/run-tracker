from aiogram.fsm.state import State, StatesGroup


class AddingUTCOffset(StatesGroup):
    choosing_timezone = State()


class AddingActivity(StatesGroup):
    entering_date = State()
    entering_time = State()
    entering_lap_times = State()
    confirming_result = State()
