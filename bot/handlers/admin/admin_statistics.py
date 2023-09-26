from aiogram import types
from bot.loader import dp
from bot.utils.mysql import db
from bot.filters import IsAdminUser
from aiogram.dispatcher.filters.builtin import Text


@dp.message_handler(IsAdminUser(), Text('Статистика'))
async def admin_statistics(message: types.Message):
    count_users = await db.get_count_users()
    count_dead_users = await db.get_count_dead_users()
    count_alive_users = await db.get_count_alive_users()
    count_random_users = await db.get_count_random_users()
    statistic_message = f'📊 Статистика:\n' \
                        f'• Всего: {count_users}\n' \
                        f'• Случаных пользователей: {count_random_users}\n'\
                        f'• Живы: {count_alive_users}\n' \
                        f'• Мертвы: {count_dead_users}'
    await message.answer(statistic_message)