from aiogram.utils import executor
from bot.loader import on_startup, bot
from bot.handlers import dp
from bot.utils.other import SenderList



sender_list = SenderList(bot)

if __name__ == '__main__':
    bot['sender_list'] = sender_list
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)