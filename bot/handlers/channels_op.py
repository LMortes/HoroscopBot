from aiogram import types
from bot.loader import dp
from bot.utils.mysql import db
from bot.loader import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def check_subscribe_channels(user_id):
    global chat_member
    is_subscribed = await db.get_subscribed_op(user_id)
    channels = await db.get_channels_op()
    channels_not_sub = []
    for channel in channels:
        try:
            chat_member = await bot.get_chat_member(chat_id=channel[2], user_id=user_id)
        except Exception as error:
            print(error)
        if chat_member['status'] == 'left':
            channels_not_sub.append(channel)
    if bool(len(channels_not_sub)):
        if is_subscribed == 1:
            await db.change_subscribed_op(user_id, 0)
        await send_subscribe_channels_message(user_id, channels_not_sub)
    if is_subscribed == 0 and not len(channels_not_sub):
        await db.change_subscribed_op(user_id, 1)
    return bool(len(channels_not_sub))


async def send_subscribe_channels_message(user_id, channels_not_sub):
    ikb_channels_op = InlineKeyboardMarkup(row_width=2)
    lang = await db.get_user_lang(user_id)
    for channel in channels_not_sub:
        channel_button = InlineKeyboardButton(text=channel[1], url=channel[3])
        ikb_channels_op.insert(channel_button)
    channel_button_continue = InlineKeyboardButton(text=f'{_("Продолжить", lang)}', callback_data='continue_channels_op')
    ikb_channels_op.add(channel_button_continue)
    await bot.send_message(user_id, _('😔 <b>Вы еще не подписаны на наши каналы</b>\n\n<i>Подпишись и нажми «Продолжить»!</i>', lang), reply_markup=ikb_channels_op)


@dp.callback_query_handler(lambda callback: callback.data == 'continue_channels_op')
async def continue_channels_op(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    if not await check_subscribe_channels(callback.from_user.id):  # Если пользователь подписался на все каналы, то выводится навигация если нет то в функции check... вся логика и дальнейшие действия
        lang = await db.get_user_lang(callback.from_user.id)
        await callback.message.answer(_('Просто отправьте мне имя артиста и/или название композиции, и я найду эту композицию!\n'
                               '/song - поиск по композициям\n'
                               '/artist - поиск по исполнителям\n'
                               '/setlang - изменить язык\n'
                               '/settings - изменить настройки', lang))
    return
