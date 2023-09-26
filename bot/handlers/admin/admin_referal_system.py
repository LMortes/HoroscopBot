import os
import re
from aiogram import types
from bot.loader import dp, bot
from bot.utils.mysql import db
from bot.filters import IsAdminUser
from aiogram.dispatcher import FSMContext
from bot.keyboards import inline as ikb
from aiogram.dispatcher.filters.builtin import Text

from bot.utils.states.add_ref_link_state import StepsAddRefLink


@dp.message_handler(IsAdminUser(), Text('Рефералы'))
async def referal_system_info(message: types.Message):
    await message.answer('Реферальные ссылки\n\n'
                         'Чтобы добавить реферальную ссылку, введи команду - /add_ref', reply_markup=await ikb.ikb_referals_links())


@dp.callback_query_handler(IsAdminUser(), lambda callback: callback.data.startswith('referal_link_'))
async def referal_link(callback: types.CallbackQuery, state: FSMContext):
    ref_link_id = callback.data[13:]
    referal_link_info = await db.get_referal_link_info_by_id(ref_link_id)

    name_link = referal_link_info[1]
    all_users = referal_link_info[3]
    unique_users = referal_link_info[2]
    ref_users_alive = await db.get_ref_users_alive(name_link)
    ref_users_op = await db.get_ref_users_op(name_link)
    ref_hour, ref_day = await db.get_unique_users_hour_and_day(name_link)

    await state.update_data(ref_link_id=ref_link_id)
    result_message = f'Данные реферальной ссылки.\n\n' \
                     f'Название ссылки: {name_link}\n\n' \
                     f'📊 Статистика:\n' \
                     f'• Всего перешли: {all_users}\n' \
                     f'• Из них уникальных переходов: {unique_users}\n' \
                     f'• Из них живы: {ref_users_alive}\n' \
                     f'• Из них подписались на ОП: {ref_users_op}\n\n' \
                     f'👤 Статистика по времени:\n' \
                     f'• За последний час: {ref_hour}\n' \
                     f'• За последние 24 часа: {ref_day}\n\n' \
                     f'Ссылка: <code>https://t.me/{os.getenv("BOT_LINK")}?start={name_link}</code>'

    await bot.edit_message_text(result_message, callback.message.chat.id, callback.message.message_id, reply_markup=ikb.InlineKeyboardMarkup(inline_keyboard=[
        [
            ikb.InlineKeyboardButton(text='🗑 Удалить', callback_data='referal_delete')
        ],
        [
            ikb.InlineKeyboardButton(text='◀️ Назад', callback_data='referal_back')
        ],
    ]))


@dp.callback_query_handler(IsAdminUser(), lambda callback: callback.data == 'referal_delete')
async def delete_referal_link(callback: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text('Точно удаляем? Подтверди свое действие.', callback.message.chat.id, callback.message.message_id, reply_markup=ikb.InlineKeyboardMarkup(inline_keyboard=[
        [
            ikb.InlineKeyboardButton(text='Удаляем', callback_data='confirm_referal_delete')
        ],
        [
            ikb.InlineKeyboardButton(text='Отмена', callback_data='confirm_referal_cancel')
        ],
    ]))


@dp.callback_query_handler(IsAdminUser(), lambda callback: callback.data == 'confirm_referal_delete')
async def confirm_delete_referal_link(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ref_id = data["ref_link_id"]
    await db.delete_referal_link(ref_id)
    await bot.edit_message_text('Реферальная ссылка успешно удалена!', callback.message.chat.id, callback.message.message_id)
    await state.reset_data()


@dp.callback_query_handler(IsAdminUser(), lambda callback: callback.data == 'confirm_referal_cancel')
async def confirm_delete_referal_link(callback: types.CallbackQuery, state: FSMContext):
    await state.reset_data()
    await bot.edit_message_text('Действие отменено.', callback.message.chat.id, callback.message.message_id)


@dp.callback_query_handler(IsAdminUser(), lambda callback: callback.data == 'referal_back')
async def back_referals_links(callback: types.CallbackQuery):
    await bot.edit_message_text('Реферальные ссылки\n\n'
                                'Чтобы добавить реферальную ссылку, введи команду - /add_ref', callback.message.chat.id, callback.message.message_id,
                                reply_markup=await ikb.ikb_referals_links())


@dp.message_handler(IsAdminUser(), commands=['add_ref'])
async def add_ref_link(message: types.Message, state:FSMContext):
    await message.answer('Введи название ссылки.\n\n'
                         '❗️ Название ссылки должно быть исключительно на английском языке\n'
                         '❗️ Название ссылки не должно содержать пробелов, смайлов, и т.п.\n'
                         '❗️ Использовать _ или - и цифры в названии ссылки можно\n'
                         '⚠️ Так же не советуется использовать ссылки состоящие только из цифр, так как обычная реферальная система может с ними конфликтовать')
    await state.set_state(StepsAddRefLink.get_ref_name)


@dp.message_handler(IsAdminUser(), state=StepsAddRefLink.get_ref_name)
async def get_name_ref_link(message: types.Message, state: FSMContext):
    result_link = message.text.replace(" ", "")
    result_link = result_link.lower()
    if re.match(r'^[a-zA-Z\d_-]+$', result_link):
        await message.answer('Записал новую реферальную ссылку в базу данных.')
        await db.add_referal_link(result_link)
    else:
        return await message.answer('❗️ Некорректная ссылка. В ссылке содержатся недопустимые символы. Введи название ссылки еще раз.')
    await state.finish()


