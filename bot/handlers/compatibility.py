from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.bin.compatibility_db import compatibility_caption
from bot.filters import IsNotAdminUser
from bot.handlers.channels_op import check_subscribe_channels
from aiogram.dispatcher.filters.builtin import Text
from bot.keyboards import inline as ikb
from bot.loader import bot, dp
from bot.utils.mysql import db


@dp.message_handler(IsNotAdminUser(), Text('💟 Совместимость'))
async def compatibility_handler(message: types.Message):
    if not await check_subscribe_channels(message.from_user.id):
        with open('bot/images/compatibility.jpg', 'rb') as compatibility:
            await bot.send_photo(message.chat.id, compatibility, '💟 Совместимость\n\n'
                                                                 'Между ___ и ___\n\n'
                                                                 '🎲 Выберите два знака зодиака',
                                 reply_markup=await ikb.compatibility_keyboard())


@dp.callback_query_handler(IsNotAdminUser(), lambda callback: callback.data.startswith('comp_'))
async def compatibility_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    first_sign = ''
    second_sign = ''
    sign = ''
    text_message = callback.message.caption
    message_callback = callback.data[5:]
    if message_callback == 'aries':
        sign = '♈️ Овен'
    elif message_callback == 'taurus':
        sign = '♉️ Телец'
    elif message_callback == 'twins':
        sign = '♊️ Близнецы'
    elif message_callback == 'cancer':
        sign = '♋️ Рак'
    elif message_callback == 'leo':
        sign = '♌️ Лев'
    elif message_callback == 'maiden':
        sign = '♍️ Дева'
    elif message_callback == 'libra':
        sign = '♎️ Весы'
    elif message_callback == 'scorpio':
        sign = '♏️ Скорпион'
    elif message_callback == 'sagittarius':
        sign = '♐️ Стрелец'
    elif message_callback == 'capricorn':
        sign = '♑️ Козерог'
    elif message_callback == 'aquarius':
        sign = '♒️ Водолей'
    elif message_callback == 'pisces':
        sign = '♓️ Рыбы'

    if '___ и ___' in text_message:
        try:
            await bot.edit_message_caption(callback.message.chat.id, callback.message.message_id,
                                       caption='💟 Совместимость\n\n'
                                               f'Между {sign} и ___\n\n'
                                               '🎲 Выберите два знака зодиака',
                                       reply_markup=await ikb.compatibility_keyboard())
        except:
            pass
    else:
        middle_split = text_message.split('Между ')[1]
        first_sign = (middle_split.split(' и ___')[0]).strip()
        second_sign = sign

        compatibility = {
            "♈️ Овен": {
                "♈️ Овен": 1,
                "♉️ Телец": 2,
                "♊️ Близнецы": 3,
                "♋️ Рак": 4,
                "♌️ Лев": 5,
                "♍️ Дева": 6,
                "♎️ Весы": 7,
                "♏️ Скорпион": 8,
                "♐️ Стрелец": 9,
                "♑️ Козерог": 10,
                "♒️ Водолей": 11,
                "♓️ Рыбы": 12,
            },
            "♉️ Телец": {
                "♈️ Овен": 2,
                "♉️ Телец": 13,
                "♊️ Близнецы": 14,
                "♋️ Рак": 15,
                "♌️ Лев": 16,
                "♍️ Дева": 17,
                "♎️ Весы": 18,
                "♏️ Скорпион": 19,
                "♐️ Стрелец": 20,
                "♑️ Козерог": 21,
                "♒️ Водолей": 22,
                "♓️ Рыбы": 23,
            },
            "♊️ Близнецы": {
                "♈️ Овен": 3,
                "♉️ Телец": 14,
                "♊️ Близнецы": 24,
                "♋️ Рак": 25,
                "♌️ Лев": 26,
                "♍️ Дева": 27,
                "♎️ Весы": 28,
                "♏️ Скорпион": 29,
                "♐️ Стрелец": 30,
                "♑️ Козерог": 31,
                "♒️ Водолей": 32,
                "♓️ Рыбы": 33,
            },
            "♋️ Рак": {
                "♈️ Овен": 4,
                "♉️ Телец": 15,
                "♊️ Близнецы": 25,
                "♋️ Рак": 34,
                "♌️ Лев": 35,
                "♍️ Дева": 36,
                "♎️ Весы": 37,
                "♏️ Скорпион": 38,
                "♐️ Стрелец": 39,
                "♑️ Козерог": 40,
                "♒️ Водолей": 41,
                "♓️ Рыбы": 42,
            },
            "♌️ Лев": {
                "♈️ Овен": 5,
                "♉️ Телец": 16,
                "♊️ Близнецы": 26,
                "♋️ Рак": 35,
                "♌️ Лев": 43,
                "♍️ Дева": 44,
                "♎️ Весы": 45,
                "♏️ Скорпион": 46,
                "♐️ Стрелец": 47,
                "♑️ Козерог": 48,
                "♒️ Водолей": 49,
                "♓️ Рыбы": 50,
            },
            "♍️ Дева": {
                "♈️ Овен": 6,
                "♉️ Телец": 17,
                "♊️ Близнецы": 27,
                "♋️ Рак": 36,
                "♌️ Лев": 44,
                "♍️ Дева": 51,
                "♎️ Весы": 52,
                "♏️ Скорпион": 53,
                "♐️ Стрелец": 54,
                "♑️ Козерог": 55,
                "♒️ Водолей": 56,
                "♓️ Рыбы": 57,
            },
            "♎️ Весы": {
                "♈️ Овен": 7,
                "♉️ Телец": 18,
                "♊️ Близнецы": 28,
                "♋️ Рак": 37,
                "♌️ Лев": 45,
                "♍️ Дева": 52,
                "♎️ Весы": 58,
                "♏️ Скорпион": 59,
                "♐️ Стрелец": 60,
                "♑️ Козерог": 61,
                "♒️ Водолей": 62,
                "♓️ Рыбы": 63,
            },
            "♏️ Скорпион": {
                "♈️ Овен": 8,
                "♉️ Телец": 19,
                "♊️ Близнецы": 29,
                "♋️ Рак": 38,
                "♌️ Лев": 46,
                "♍️ Дева": 53,
                "♎️ Весы": 59,
                "♏️ Скорпион": 64,
                "♐️ Стрелец": 65,
                "♑️ Козерог": 66,
                "♒️ Водолей": 67,
                "♓️ Рыбы": 68,
            },
            "♐️ Стрелец": {
                "♈️ Овен": 9,
                "♉️ Телец": 20,
                "♊️ Близнецы": 30,
                "♋️ Рак": 39,
                "♌️ Лев": 47,
                "♍️ Дева": 54,
                "♎️ Весы": 60,
                "♏️ Скорпион": 65,
                "♐️ Стрелец": 69,
                "♑️ Козерог": 70,
                "♒️ Водолей": 71,
                "♓️ Рыбы": 72,
            },
            "♑️ Козерог": {
                "♈️ Овен": 10,
                "♉️ Телец": 21,
                "♊️ Близнецы": 31,
                "♋️ Рак": 40,
                "♌️ Лев": 48,
                "♍️ Дева": 55,
                "♎️ Весы": 61,
                "♏️ Скорпион": 66,
                "♐️ Стрелец": 70,
                "♑️ Козерог": 73,
                "♒️ Водолей": 74,
                "♓️ Рыбы": 75,
            },
            "♒️ Водолей": {
                "♈️ Овен": 11,
                "♉️ Телец": 22,
                "♊️ Близнецы": 32,
                "♋️ Рак": 41,
                "♌️ Лев": 49,
                "♍️ Дева": 56,
                "♎️ Весы": 62,
                "♏️ Скорпион": 67,
                "♐️ Стрелец": 71,
                "♑️ Козерог": 74,
                "♒️ Водолей": 76,
                "♓️ Рыбы": 77,
            },
            "♓️ Рыбы": {
                "♈️ Овен": 12,
                "♉️ Телец": 23,
                "♊️ Близнецы": 33,
                "♋️ Рак": 42,
                "♌️ Лев": 50,
                "♍️ Дева": 57,
                "♎️ Весы": 63,
                "♏️ Скорпион": 68,
                "♐️ Стрелец": 72,
                "♑️ Козерог": 75,
                "♒️ Водолей": 77,
                "♓️ Рыбы": 78,
            },
        }
        compatibility_number = compatibility[f'{first_sign}'][f'{second_sign}']
        compatibility_text = compatibility_caption[compatibility_number]
        try:
            await bot.edit_message_caption(callback.message.chat.id, callback.message.message_id,
                                       caption='💟 Совместимость\n\n'
                                               f'Между {first_sign} и {second_sign}\n\n'
                                               f'🎲 Выберите два знака зодиака\n\n{compatibility_text}')
        except:
            pass
