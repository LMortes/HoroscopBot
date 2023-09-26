from aiogram import types
from bot.loader import dp
from bot.utils.mysql import db
from bot.filters import IsAdminUser
from aiogram.dispatcher import FSMContext
from bot.utils.states import StepsChannelsOp
from bot.keyboards import inline as ikb
from aiogram.dispatcher.filters.builtin import Text


@dp.message_handler(IsAdminUser(), Text('Обяз. Подписка'))
async def admin_channels_op(message: types.Message):
    channels_op = await db.get_channels_op()
    message_channels_op = 'Каналы на обязательной подписке:\n\n'
    channels_message = ''
    for channel in channels_op:
        channels_message += f'{channel[0]}. {channel[1]}\n{channel[3]}\n\n'
    result_message_channels_op = message_channels_op + channels_message
    await message.answer(result_message_channels_op, reply_markup=ikb.ikb_admin_channels_op_edit, disable_web_page_preview=True)


@dp.callback_query_handler(IsAdminUser(), lambda callback: callback.data.startswith('admin_chan_op_'))
async def channels_op_edit_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data[14:] == 'add':
        await callback.message.edit_text('Сейчас тебе потребуется ввести название канала, id канала и ссылку на канал в следующем формате:\n\n'
                                         'Название|id|ссылка\n\n'
                                         'ID канала ты сможешь взять например у бота userinfobot, переслав ему сообщение из канала или отправив ссылку.\n'
                                         '❗️❗️❗️ Обязательно, перед добавлением канала в ОП убедись, что ты дал фулл админку своему боту в том канале, который собираешься добавлять')
        await callback.answer()
        await state.set_state(StepsChannelsOp.get_channel_op)
    elif callback.data[14:] == 'delete':
        await callback.message.edit_reply_markup(reply_markup=await ikb.admin_delete_channels_op_keyboard(await db.get_channels_op()))


@dp.callback_query_handler(IsAdminUser(), lambda callback: callback.data.startswith('channel_op_delete_'))
async def delete_channel_op(callback: types.CallbackQuery):
    channel_id = callback.data[18:]
    await db.delete_channel_op(channel_id)
    await callback.message.answer('Канал успешно удален!')
    await callback.answer()



@dp.message_handler(IsAdminUser(), state=StepsChannelsOp.get_channel_op)
async def validate_channel_op(message: types.Message, state: FSMContext):
    channel_info = message.text.split('|')
    try:
        await db.add_channel_op(channel_info)
    except:
        await state.finish()
        return await message.answer('❗️ Некорректный ввод')
    await message.answer('Канал успешно добавлен!')
    channels_op = await db.get_channels_op()
    message_channels_op = 'Каналы на обязательной подписке:\n\n'
    channels_message = ''
    for channel in channels_op:
        channels_message += f'{channel[0]}. {channel[1]}\n{channel[3]}\n\n'
    result_message_channels_op = message_channels_op + channels_message
    await message.answer(result_message_channels_op, reply_markup=ikb.ikb_admin_channels_op_edit)
    await state.finish()

