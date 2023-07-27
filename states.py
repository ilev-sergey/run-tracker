from aiogram.fsm.state import StatesGroup, State


class UTC_Offset(StatesGroup):
    choosing_timezone = State()
