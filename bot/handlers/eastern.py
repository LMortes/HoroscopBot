from aiogram import types
from bot.filters import IsNotAdminUser
from bot.handlers.channels_op import check_subscribe_channels
from aiogram.dispatcher.filters.builtin import Text
from bot.keyboards import inline as ikb
from bot.loader import bot, dp
from bot.bin import eastern_predictions as ep
from bot.utils.mysql import db


@dp.message_handler(IsNotAdminUser(), Text('🏵 Восточный гороскоп'))
async def eastern_handler(message: types.Message):
    if not await check_subscribe_channels(message.from_user.id):
        with open('bot/images/eastern.jpg', 'rb') as eastern:
            await bot.send_photo(message.chat.id, eastern, '🎲 <b>Выберете животное по году Вашего рождения и получите предсказание на год</b>', reply_markup=await ikb.ikb_eastern())


@dp.callback_query_handler(IsNotAdminUser(), lambda callback: callback.data.startswith('eastern_'))
async def eastern_callback(callback: types.CallbackQuery):
    message_callback = callback.data[8:]
    await callback.answer()
    if message_callback == 'mouse':
        await callback.message.answer(ep[f'{message_callback}'])
    elif message_callback == 'bull':
        await callback.message.answer(ep[f'{message_callback}'])
    elif message_callback == 'tiger':
        await callback.message.answer(ep[f'{message_callback}'])
    elif message_callback == 'rabbit':
        await callback.message.answer(ep[f'{message_callback}'])
    elif message_callback == 'dragon':
        await callback.message.answer(ep[f'{message_callback}'])
    elif message_callback == 'snake':
        await callback.message.answer(ep[f'{message_callback}'])
    elif message_callback == 'horse':
        await callback.message.answer(ep[f'{message_callback}'])
    elif message_callback == 'goat':
        await callback.message.answer(ep[f'{message_callback}'])
    elif message_callback == 'monkey':
        await callback.message.answer(ep[f'{message_callback}'])
    elif message_callback == 'cock':
        await callback.message.answer(ep[f'{message_callback}'])
    elif message_callback == 'dog':
        await callback.message.answer(ep[f'{message_callback}'])
    elif message_callback == 'pig':
        await callback.message.answer(ep[f'{message_callback}'])