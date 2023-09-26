import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.bin.compatibility_db import compatibility_caption
from bot.filters import IsNotAdminUser
from bot.handlers.channels_op import check_subscribe_channels
from aiogram.dispatcher.filters.builtin import Text
from bot.keyboards import inline as ikb
from bot.loader import bot, dp
from bot.bin.taro_db import taro
from bot.bin.prediction_db import predictions
from bot.utils.mysql import db


@dp.message_handler(IsNotAdminUser(), Text('🀄️ Карты таро'))
async def taro_handler(message: types.Message):
    if not await check_subscribe_channels(message.from_user.id):
        random_numbers = random.sample(range(1, 5), 4)
        random_numbers = sorted(random_numbers)
        taro_keyboard = await ikb.taro_ikb(random_numbers)
        with open('bot/images/taro/main_taro.jpg', 'rb') as magic_number:
            await bot.send_photo(message.chat.id, magic_number, '<b>🀄️ Выбери карту, которая понравилась больше всего 👀</b>', reply_markup=taro_keyboard)


@dp.callback_query_handler(IsNotAdminUser(), lambda callback: callback.data == 'taro')
async def taro_callback(callback: types.CallbackQuery):
    await callback.answer()
    random_taro_number = (random.sample(range(1, 27), 1))[0] # 27
    try:
        with open(f'bot/images/taro/{taro[random_taro_number]["image"]}.jpg', 'rb') as taro_image:
            await bot.send_photo(callback.message.chat.id, taro_image, f'{taro[random_taro_number]["taro_text"]}')
    except:
        pass