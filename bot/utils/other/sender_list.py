import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import RetryAfter, MessageNotModified, BotBlocked
from bot.utils.mysql import db

class SenderList:
    def __init__(self, bot):
        self.bot = bot

    async def add_keyboard(self, info_buttons):
        added_keyboard = InlineKeyboardMarkup(row_width=1)
        buttons = info_buttons.split('||')
        text_button_sender = []
        url_button_sender = []
        for buttons in buttons:
            text, url = buttons.split('|')
            text_button_sender.append(text)
            url_button_sender.append(url)
        for text, url in zip(text_button_sender, url_button_sender):
            add_button = InlineKeyboardButton(text=text, url=url)
            added_keyboard.insert(add_button)
        return added_keyboard

    async def get_users(self, name_sender):
        user_ids = await db.get_users_for_sender(name_sender)
        if user_ids != False:
            return user_ids
        else:
            return False

    async def send_message(self, user_id: int, from_chat_id: int, message_id: int, name_sender: str, keyboard: InlineKeyboardMarkup = None):
        try:
            await self.bot.copy_message(user_id, from_chat_id, message_id, reply_markup=keyboard)

        except RetryAfter as e:
            await asyncio.sleep(e.timeout)
            print(e)
            return await self.send_message(user_id, from_chat_id, message_id, name_sender, keyboard)
        except MessageNotModified as e:
            await db.change_active_user(user_id, 0, name_sender, 'unsuccesful', f'{e}')
            print(e)
        except BotBlocked as e:
            await db.change_active_user(user_id, 0, name_sender, 'unsuccesful', f'{e}')
            print(e)
        except Exception as e:
            await db.change_active_user(user_id, 0, name_sender, 'unsuccesful', f'{e}')
            print(e)
        else:
            await db.change_active_user(user_id, 1, name_sender, 'success', 'No errors')
            return True
        return False

    async def broadcaster(self, name_sender: str, from_chat_id: int, message_id: int, info_buttons: str = None):
        keyboard = None

        if info_buttons is not None:
            keyboard = await self.add_keyboard(info_buttons)
        user_ids = await self.get_users(name_sender)
        count = 0
        try:
            for user_id in user_ids:
                if await self.send_message(int(user_id[0]), from_chat_id, message_id, name_sender, keyboard):
                    count += 1
                await asyncio.sleep(.05)
        except:
            pass
        finally:
            pass
            # какие то действия после успешной рассылки

        return count
