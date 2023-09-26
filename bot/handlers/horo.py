import datetime

import httpx
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.bin.compatibility_db import compatibility_caption
from bot.filters import IsNotAdminUser
from bs4 import BeautifulSoup
from bot.handlers.channels_op import check_subscribe_channels
from aiogram.dispatcher.filters.builtin import Text
from bot.keyboards import default as kb
from bot.keyboards import inline as ikb
from bot.loader import bot, dp
from bot.bin.prediction_db import predictions
from bot.utils.mysql import db


headers = {
    'accept_language': 'ru-RU,ru;q=0.9, en-US;q=0.8,en;q=0.7',
    'user_agent': 'Mozilla/5.0 (Linux; Android 12; moto g22 Build/STA32.79-77-28-18; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166 Mobile Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}

async def get_response(link):
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as htx:
        result = await htx.get(url=link)
        if result.status_code != 200:
            return await get_response(link=link)
        else:
            return await result.aread()

async def get_goroscop(sign_type, calendar):
    link = f'https://horo.mail.ru/prediction/{sign_type}/{calendar}/'

    result_response = await get_response(link)
    beautifulSoup = BeautifulSoup(markup=result_response, features='lxml')

    text_horo = beautifulSoup.find(name='div', class_='article__text')
    parse_text_horo = text_horo.find_all(name='p')
    horo_texts = []
    for horo in parse_text_horo:
        horo_texts.append(horo.text)
    return horo_texts


async def generate_horo_message(sign_text, sign_type, calendar='today'):
    horo_arr = await get_goroscop(sign_type, calendar)
    formatted_date = ''

    if calendar == 'today':
        today = datetime.date.today()
        formatted_date = today.strftime('%d.%m.%Y')
    elif calendar == 'tomorrow':
        formatted_date = 'завтра'
    elif calendar == 'week':
        formatted_date = 'неделю'
    elif calendar == 'month':
        formatted_date = 'месяц'
    elif calendar == 'year':
        formatted_date = 'год'

    result_horo_message = f'<b>{sign_text}</b> на {formatted_date}\n\n'
    for horo in horo_arr:
        result_horo_message += f'🔮 {horo}\n\n'
    return result_horo_message




@dp.message_handler(IsNotAdminUser(), Text('🔮 Гороскоп'))
async def horo_handler(message: types.Message):
    if not await check_subscribe_channels(message.from_user.id):
        with open('bot/images/horo.jpg', 'rb') as horo:
            await bot.send_photo(message.chat.id, horo, '<b>🔮 Выберите Ваш знак зодиака, чтобы узнать гороскоп на сегодня</b>', reply_markup=kb.horo_kb)


@dp.message_handler(IsNotAdminUser(), Text('♈️ Овен'))
async def aries_handler(message: types.Message):
    sign_type = 'aries'
    result_horo_message = await generate_horo_message(message.text, sign_type)
    await message.answer(result_horo_message, reply_markup=await ikb.ikb_horoscop_calendar())


@dp.message_handler(IsNotAdminUser(), Text('♉️ Телец'))
async def taurus_handler(message: types.Message):
    sign_type = 'taurus'
    result_horo_message = await generate_horo_message(message.text, sign_type)
    await message.answer(result_horo_message, reply_markup=await ikb.ikb_horoscop_calendar())


@dp.message_handler(IsNotAdminUser(), Text('♊️ Близнецы'))
async def twins_handler(message: types.Message):
    sign_type = 'gemini'
    result_horo_message = await generate_horo_message(message.text, sign_type)
    await message.answer(result_horo_message, reply_markup=await ikb.ikb_horoscop_calendar())


@dp.message_handler(IsNotAdminUser(), Text('♋️ Рак'))
async def cancer_handler(message: types.Message):
    sign_type = 'cancer'
    result_horo_message = await generate_horo_message(message.text, sign_type)
    await message.answer(result_horo_message, reply_markup=await ikb.ikb_horoscop_calendar())


@dp.message_handler(IsNotAdminUser(), Text('♌️ Лев'))
async def leo_handler(message: types.Message):
    sign_type = 'leo'
    result_horo_message = await generate_horo_message(message.text, sign_type)
    await message.answer(result_horo_message, reply_markup=await ikb.ikb_horoscop_calendar())


@dp.message_handler(IsNotAdminUser(), Text('♍️ Дева'))
async def maiden_handler(message: types.Message):
    sign_type = 'virgo'
    result_horo_message = await generate_horo_message(message.text, sign_type)
    await message.answer(result_horo_message, reply_markup=await ikb.ikb_horoscop_calendar())


@dp.message_handler(IsNotAdminUser(), Text('♎️ Весы'))
async def libra_handler(message: types.Message):
    sign_type = 'libra'
    result_horo_message = await generate_horo_message(message.text, sign_type)
    await message.answer(result_horo_message, reply_markup=await ikb.ikb_horoscop_calendar())


@dp.message_handler(IsNotAdminUser(), Text('♏️ Скорпион'))
async def scorpio_handler(message: types.Message):
    sign_type = 'scorpio'
    result_horo_message = await generate_horo_message(message.text, sign_type)
    await message.answer(result_horo_message, reply_markup=await ikb.ikb_horoscop_calendar())


@dp.message_handler(IsNotAdminUser(), Text('♐️ Стрелец'))
async def sagittarius_handler(message: types.Message):
    sign_type = 'sagittarius'
    result_horo_message = await generate_horo_message(message.text, sign_type)
    await message.answer(result_horo_message, reply_markup=await ikb.ikb_horoscop_calendar())


@dp.message_handler(IsNotAdminUser(), Text('♑️ Козерог'))
async def capricorn_handler(message: types.Message):
    sign_type = 'capricorn'
    result_horo_message = await generate_horo_message(message.text, sign_type)
    await message.answer(result_horo_message, reply_markup=await ikb.ikb_horoscop_calendar())


@dp.message_handler(IsNotAdminUser(), Text('♒️ Водолей'))
async def aquarius_handler(message: types.Message):
    sign_type = 'aquarius'
    result_horo_message = await generate_horo_message(message.text, sign_type)
    await message.answer(result_horo_message, reply_markup=await ikb.ikb_horoscop_calendar())


@dp.message_handler(IsNotAdminUser(), Text('♓️ Рыбы'))
async def pisces_handler(message: types.Message):
    sign_type = 'pisces'
    result_horo_message = await generate_horo_message(message.text, sign_type)
    await message.answer(result_horo_message, reply_markup=await ikb.ikb_horoscop_calendar())


@dp.callback_query_handler(IsNotAdminUser(), lambda callback: callback.data.startswith('horo_cal_'))
async def calendar_horo_callback(callback: types.CallbackQuery):
    message_callback = callback.data[9:]
    zodiac = (callback.message.text).split(' на')[0]
    sign_type = ''
    if zodiac == '♈️ Овен':
        sign_type = 'aries'
    elif zodiac == '♉️ Телец':
        sign_type = 'taurus'
    elif zodiac == '♊️ Близнецы':
        sign_type = 'twins'
    elif zodiac == '♋️ Рак':
        sign_type = 'cancer'
    elif zodiac == '♌️ Лев':
        sign_type = 'leo'
    elif zodiac == '♍️ Дева':
        sign_type = 'maiden'
    elif zodiac == '♎️ Весы':
        sign_type = 'libra'
    elif zodiac == '♏️ Скорпион':
        sign_type = 'scorpio'
    elif zodiac == '♐️ Стрелец':
        sign_type = 'sagittarius'
    elif zodiac == '♑️ Козерог':
        sign_type = 'capricorn'
    elif zodiac == '♒️ Водолей':
        sign_type = 'aquarius'
    elif zodiac == '♓️ Рыбы':
        sign_type = 'pisces'

    calendar = message_callback
    result_horo_message = await generate_horo_message(zodiac, sign_type, calendar)
    try:
        await bot.edit_message_text(result_horo_message, callback.message.chat.id, callback.message.message_id, reply_markup=await ikb.ikb_horoscop_calendar())
    except:
        pass
    await callback.answer()