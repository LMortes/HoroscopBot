import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.bin.compatibility_db import compatibility_caption
from bot.filters import IsNotAdminUser
from bot.handlers.channels_op import check_subscribe_channels
from aiogram.dispatcher.filters.builtin import Text
from bot.keyboards import inline as ikb
from bot.loader import bot, dp
from bot.bin.prediction_db import predictions
from bot.utils.mysql import db


async def generate_prediction_text():
    random_prediction = random.choice(predictions)
    return random_prediction


@dp.message_handler(IsNotAdminUser(), Text('🟣 Магия чисел'))
async def magic_numbers_handler(message: types.Message):
    if not await check_subscribe_channels(message.from_user.id):
        random_numbers = random.sample(range(1, 100), 5)
        random_numbers = sorted(random_numbers)
        number_1, number_2, number_3, number_4, number_5 = random_numbers
        magic_numbers_keyboard = await ikb.magic_numbers_ikb(random_numbers)
        with open('bot/images/magic_number.jpg', 'rb') as magic_number:
            await bot.send_photo(message.chat.id, magic_number, '<b>🟣 Магия чисел</b>\n\n'
                                                                f'Ваши числа: <b><i>{number_1} {number_2} {number_3} {number_4} {number_5}</i></b>\n\n'
                                                                '🎲 Выберите любое число из списка ниже и получите свое предсказание', reply_markup=magic_numbers_keyboard)


@dp.callback_query_handler(IsNotAdminUser(), lambda callback: callback.data == 'magic_number')
async def magic_number_callback(callback: types.CallbackQuery):
    await callback.answer()
    prediction_text = await generate_prediction_text()

    await callback.message.answer('<b>🔮 Ваше предсказание</b>\n\n'
                                  f'💬 {prediction_text}')

