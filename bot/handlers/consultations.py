from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.bin.compatibility_db import compatibility_caption
from bot.filters import IsNotAdminUser
from bot.handlers.channels_op import check_subscribe_channels
from aiogram.dispatcher.filters.builtin import Text
from bot.keyboards import inline as ikb
from bot.keyboards import default as kb
from bot.loader import bot, dp
from bot.utils.mysql import db
from bot.utils.states.code_love import CodeLove
from bot.utils.states.personal_cons import PersonalCons


@dp.message_handler(IsNotAdminUser(), Text('🏠 Главное меню'), state=['*'])
async def goto_main_menu_handler(message: types.Message, state: FSMContext):
    await state.finish()
    if not await check_subscribe_channels(message.from_user.id):
        await message.answer('🏚 Вы в главном меню', reply_markup=kb.main_menu_keyboard)



@dp.message_handler(IsNotAdminUser(), Text('🪬 Личные консультации'))
async def consultations_handler(message: types.Message):
    if not await check_subscribe_channels(message.from_user.id):
        with open('bot/images/cons.jpg', 'rb') as cons:
            await bot.send_photo(message.chat.id, cons, '❔Вы можете заказать индивидуальную консультацию и получить ответы на интересующие Вас личные вопросы!',
                                 reply_markup=kb.cons_kb)


@dp.message_handler(IsNotAdminUser(), Text('🔮 Персональный гороскоп на 2023 год'))
async def personal_horo_handler(message: types.Message, state: FSMContext):
    await state.set_state(PersonalCons.get_text)
    await message.answer('<b>🔮 Персональный гороскоп на 2023 год</b>\n\n'
                         'Индивидуальное астрологическое предсказание на год, с учетом Вашей точной даты рождения и места рождения.\n'
                         'Заполните, пожалуйста, форму заявки:\n'
                         '1. Максимально точную дату и время вашего рождения: день, месяц, год, час, минута. (Если не знаете точное время, укажите хотя бы приблизительно)\n'
                         '2. Место рождения: Страна, населенный пункт (ближайший город от места рождения)\n'
                         '3. Ваш Пол\n\n'
                         'Пример:\n'
                         '19.11.1998 17:05\n'
                         'Россия, г. Томск\n'
                         'Жен.', reply_markup=kb.goto_menu_kb)


@dp.message_handler(IsNotAdminUser(), Text('❤️‍🔥 Личный код любви и изобилия'))
async def code_love_cons_handler(message: types.Message, state: FSMContext):
    await state.set_state(PersonalCons.get_text)
    await message.answer('<b>❤️‍🔥 Личный код любви и изобилия</b>\n\n'
                         '«Код любви и изобилия» нумерологический обряд, который поможет Вам найти любовь или улучшить Ваши текущие отношения в паре.\n\n'
                         'Заполните, пожалуйста, форму заявки:\n'
                         'Фамилия Имя Отчество, Дата рождения: день, месяц, год\n\n'
                         'Пример:\n'
                         'Гаврикова Юлия Владимировна  19.11.1998', reply_markup=kb.goto_menu_kb)


@dp.message_handler(IsNotAdminUser(), Text('👩‍❤️‍👨 Личный код совместимости партнеров'))
async def sovmest_cons_handler(message: types.Message, state: FSMContext):
    await state.set_state(PersonalCons.get_text)
    await message.answer('<b>👩‍❤️‍👨 Личный код совместимости партнеров</b>\n\n'
                         'Для того чтобы узнать конкретно о Вашем союзе нужны две даты рождения: Ваша и партнера.\n'
                         'Заполните, пожалуйста, форму заявки:\n'
                         'Дата рождения Мужчины – день, месяц, год.\n'
                         'Дата рождения Женщины – день, месяц, год.\n\n'
                         'Пример:\n'
                         '11.06.1996\n'
                         '19.11.1998', reply_markup=kb.goto_menu_kb)



@dp.message_handler(IsNotAdminUser(), Text('🏆 Число жизненного пути'))
async def number_life_cons_handler(message: types.Message, state: FSMContext):
    await state.set_state(PersonalCons.get_text)
    await message.answer('<b>🏆 Число жизненного пути</b>\n\n'
                         'Ваше Число жизненного пути показывает, для чего вы рождены на свет!'
                         'Это ваш уникальный путь жизни. Оно рассказывает о сферах деятельности, в которых вы можете преуспеть, какими талантами и возможностями вы обладаете.\n\n'
                         'Заполните, пожалуйста, форму заявки:\n'
                         'Дата рождения: число, месяц, год.\n\n'
                         'Пример:\n'
                         '19.11.1998', reply_markup=kb.goto_menu_kb)



@dp.message_handler(IsNotAdminUser(), Text('💫 Число Судьбы (Имени)'))
async def number_name_cons_handler(message: types.Message, state: FSMContext):
    await state.set_state(PersonalCons.get_text)
    await message.answer('<b>💫 Число Судьбы (Имени)</b>\n\n'
                         'Число судьбы открывает цель вашей жизни. Ваши возможности для достижения успеха.'
                         'Ваше предназначение. Цель, к которой вы должны стремиться в жизни.\n'
                         'Число Судьбы зашифровано в вашем полном имени. Если человек меняет фамилию, меняется его предназначение.\n\n'
                         'Заполните, пожалуйста, форму заявки:\n'
                         'Фамилия Имя Отчество\n\n'
                         'Пример:\n'
                         'Гаврикова Юлия Владимировна', reply_markup=kb.goto_menu_kb)


@dp.message_handler(IsNotAdminUser(), Text('🀄️ Расклад натальной карты'))
async def natalnaya_cons_handler(message: types.Message, state: FSMContext):
    await state.set_state(PersonalCons.get_text)
    await message.answer('<b>🀄️ Расклад натальной карты</b>\n\n'
                         '<b>Натальная карта</b> представляет собой схему звездного неба в тот момент, когда вы родились\n'
                         'Она строится из расположения планет,которое влияет на судьбу,настоящее и будущее\n\n'
                         '<b>Натальная карта</b> помогает описать личность, предназначение, понять характер человека. '
                         'А если рассматривать карту в качестве прогноза, то и раскладку на будущее. '
                         'Натальная карта может дать человеку инструменты, которые можно использовать в течение своей жизни. '
                         'Например: работе,карьере, денежных вопросах, здоровье, а так же любви и отношениях.', reply_markup=kb.goto_menu_kb)

