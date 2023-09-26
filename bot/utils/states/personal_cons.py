from aiogram.dispatcher.filters.state import State, StatesGroup


class PersonalCons(StatesGroup):
    get_text = State()