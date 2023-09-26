from aiogram.dispatcher.filters.state import State, StatesGroup


class Steps(StatesGroup):
    get_name_sender = State()
    get_message = State()
    get_buttons_answer = State()
    get_count_buttons = State()
    get_info_buttons = State()
    sender_decide = State()