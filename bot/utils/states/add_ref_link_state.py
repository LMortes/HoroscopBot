from aiogram.dispatcher.filters.state import State, StatesGroup


class StepsAddRefLink(StatesGroup):
    get_ref_name = State()