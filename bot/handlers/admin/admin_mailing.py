import os
import re

from dotenv import load_dotenv
from aiogram import types
from bot.loader import dp, bot
from bot.utils.mysql import db
from bot.filters import IsAdminUser
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from bot.utils.states import Steps
from bot.utils.other import sender_list
from bot.keyboards import default as kb
from bot.keyboards import inline as ikb
from aiogram.dispatcher.filters.builtin import Text


load_dotenv()


@dp.message_handler(IsAdminUser(), commands=['admin'], state=['*'])
async def admin_functions(message: types.Message, state: FSMContext):
    await state.finish()
    return await message.answer('Админ панель', reply_markup=kb.admin_keyboard)


@dp.message_handler(IsAdminUser(), commands=['cancel_mailing'], state='*')
async def canceling_mailing(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    await message.answer('Рассылка отменена.')


@dp.message_handler(IsAdminUser(), Text('Рассылка'))
async def get_sender(message: types.Message, state: FSMContext):
    await message.answer('Введи название рассылки.\n\n⚠️ Примечание: Название рассылки ОБЯЗАТЕЛЬНО должно быть на английском языке и не должно содеражать пробелов\n\nВ рассылке пользователям название никак не фигурирует.\n\n'
                         'Так же в любой момент ты можешь прервать рассылку, просто введи  - /cancel_mailing')
    await state.set_state(Steps.get_name_sender)


@dp.message_handler(IsAdminUser(), state=Steps.get_name_sender)
async def get_sender_name_handler(message: types.Message, state: FSMContext):
    if re.match("^[A-Za-z]+$", message.text):
        await state.update_data(name_sender=message.text)
        await message.answer('Я запомнил название рассылки. Теперь введи текст рассылки')
        await state.set_state(Steps.get_message)
    else:
        return await message.answer('⚠️ Название рассылки ОБЯЗАТЕЛЬНО должно быть на английском языке и не должно содеражать пробелов\n\nВ рассылке пользователям название никак не фигурирует.\n\nВведите название рассылки заново')


@dp.message_handler(IsAdminUser(), state=Steps.get_message)
async def get_message_handler(message: types.Message, state: FSMContext):
    await state.update_data(message_sender=message.text)
    await message.answer('Я запомнил текст рассылки. Кнопки добавляем?', reply_markup=ikb.ikb_admin_sender)
    await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)
    await state.set_state(Steps.get_buttons_answer)


@dp.message_handler(IsAdminUser(), content_types=types.ContentType.PHOTO, state=Steps.get_message)
async def get_message_handler(message: types.Message, state: FSMContext):
    await message.answer('Я запомнил фото и текст рассылки. Кнопки добавляем?', reply_markup=ikb.ikb_admin_sender)
    await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)
    await state.set_state(Steps.get_buttons_answer)


@dp.message_handler(IsAdminUser(), content_types=types.ContentType.VOICE, state=Steps.get_message)
async def get_message_handler(message: types.Message, state: FSMContext):
    await message.answer('Я запомнил голосовое сообщение. Кнопки добавляем?', reply_markup=ikb.ikb_admin_sender)
    await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)
    await state.set_state(Steps.get_buttons_answer)


@dp.callback_query_handler(IsAdminUser(), lambda callback: callback.data.startswith('button_sender_'), state=Steps.get_buttons_answer)
async def get_buttons_answer_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data[14:] == 'add':
        await state.update_data(is_add_buttons=1)
        await callback.message.answer('Хорошо, я добавлю к твоей рассылке кнопки. Только теперь ответь на вопрос, сколько мне добавлять кнопок?', reply_markup=await ikb.admin_sender_count_buttons())
        await state.set_state(Steps.get_count_buttons)
    elif callback.data[14:] == 'no':
        await state.update_data(is_add_buttons=0)
        await callback.message.answer('Окей, как скажешь, без кнопок так без кнопок')
        data = await state.get_data()
        message_id = int(data.get('message_id'))
        chat_id = int(data.get('chat_id'))
        await confirm_sender(callback.message, bot, message_id, chat_id)
        await state.set_state(Steps.sender_decide)
        await callback.answer()

@dp.callback_query_handler(IsAdminUser(), lambda callback: callback.data.startswith('count_sender_buttons_'), state=Steps.get_count_buttons)
async def get_count_buttons_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        count_buttons = int(callback.data[21:])
    except:
        return await callback.message.answer('Мне нужно число кнопок -.-')
    await callback.message.answer('Введи название кнопки и ссылку в формате:\nНазвание 1 кнопки|ссылка 1 кнопки||Название 2 кнопки|ссылка 2 кнопки и т.д.')
    await state.update_data(count_buttons=count_buttons)
    await state.set_state(Steps.get_info_buttons)


@dp.message_handler(IsAdminUser(), state=Steps.get_info_buttons)
async def validate_info_buttons(message: types.Message, state: FSMContext):
    count_buttons = (await state.get_data()).get('count_buttons')
    added_keyboard = await ikb.add_keyboard_for_sender(count_buttons, message.text)
    if added_keyboard == False:
        return await message.answer('Количество кнопок не совпадает с количеством введенных данных. Введите текст и ссылки кнопок корректно как указано в примере выше')
    await state.update_data(info_buttons=message.text)
    data = await state.get_data()
    message_id = int(data.get('message_id'))
    chat_id = int(data.get('chat_id'))
    try:
        await confirm_sender(message, bot, message_id, chat_id, added_keyboard)
    except:
        await message.answer('❗️ При валидации сообщения произошла ошибка, скорее всего некорректно указаны ссылки.\n\n'
                             'Заного пришли мне текст рассылки. При заполнении кнопок будь внимателен\n\n'
                             '/cancel_mailing - отменить рассылку')
        return await state.set_state(Steps.get_message)
    await state.set_state(Steps.sender_decide)

async def confirm_sender(message: types.Message, bot: bot, message_id: int, chat_id: int, reply_markup: types.InlineKeyboardMarkup = None):
    await bot.copy_message(chat_id, chat_id, message_id, reply_markup=reply_markup)
    await message.answer('Вот сообщение для рассылки. Рассылаем?', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассылаем!', callback_data='sender_confirm')
        ],
        [
            InlineKeyboardButton(text='Отмена.', callback_data='sender_cancel')
        ]
    ]))


@dp.callback_query_handler(IsAdminUser(), lambda callback: callback.data.startswith('sender_'), state=Steps.sender_decide)
async def sender_decide(callback: types.CallbackQuery, state: FSMContext):
    senderlist = callback.bot.get('sender_list')
    data = await state.get_data()
    message_id = data.get('message_id')
    chat_id = data.get('chat_id')
    info_buttons = data.get('info_buttons')
    name_sender = data.get('name_sender')
    if callback.data[7:] == 'confirm':
        await callback.message.edit_text('Начинаю рассылку\nКак рассылка закончится, пришлю тебе сообщение.', reply_markup=None)
        if not await db.check_table_for_sender(name_sender):
            await db.create_table_for_sender(name_sender)
        count = await senderlist.broadcaster(name_sender, chat_id, message_id, info_buttons)
        await callback.message.answer(f'Рассылка прошла успешно! Сообщение отправлено {count} пользователям')
        await db.delete_table_after_sender(name_sender)

    elif callback.data[7:] == 'cancel':
        await callback.message.edit_text('Отменил рассылку', reply_markup=None)
    await state.reset_data()
    await state.finish()






