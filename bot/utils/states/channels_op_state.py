from aiogram.dispatcher.filters.state import State, StatesGroup


class StepsChannelsOp(StatesGroup):
    get_channel_op = State()