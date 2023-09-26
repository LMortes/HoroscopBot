import os
from aiogram import types
from bot.filters import IsNotAdminUser
from bot.handlers.channels_op import check_subscribe_channels
from bot.keyboards import default as kb
from bot.loader import bot, dp
from bot.utils.mysql import db


@dp.message_handler(IsNotAdminUser(), commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    names_links = await db.get_referal_link_names()
    is_user_exists = await db.user_exists(user_id)
    if not is_user_exists:
        start_command = message.text
        referrer_id = str(start_command[7:])
        if (names_links != False) and (referrer_id in names_links):
            referal_link = referrer_id
            await db.add_user(message.from_user.id, referal_link=referal_link)
            await db.add_unique_user(referal_link)
        else:
            await db.add_user(message.from_user.id)
    with open('bot/images/start_logo.jpg', 'rb') as start_logo:
        await bot.send_photo(message.chat.id, start_logo, '<b>Привет! Я - гороскоп бот </b>✨\n\n'
                                                          'Я предскажу твой день на завтра, проверю вашу совместимость с партнером, а также сделаю расклад на картах Таро 🔮', reply_markup=kb.main_menu_keyboard)




@dp.message_handler(IsNotAdminUser(), commands=['help'], state=['*'])
async def help_handler(message: types.Message):
    if not await check_subscribe_channels(message.from_user.id):
        await message.answer('❗️ Привет, я — бот гороскоп\n\n'
                             '<b>Основные команды:</b>\n\n'
                             '/horo - гороскоп на каждый день\n'
                             '/taro - карты таро\n'
                             '/numbers - магия чисел\n'
                             '/eastern - восточный гороскоп\n'
                             '/compatibility - cовместимость\n'
                             '/consultation - личные консультации\n'
                             '/menu - вернуться в главное меню')

@dp.message_handler(IsNotAdminUser(), commands=['menu'])
async def menu_handler(message: types.Message):
    if not await check_subscribe_channels(message.from_user.id):
        await message.answer('🏚 Вы в главном меню', reply_markup=kb.main_menu_keyboard)

