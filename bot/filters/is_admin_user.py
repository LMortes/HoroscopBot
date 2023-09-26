import os
from dotenv import load_dotenv
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

load_dotenv()


class IsAdminUser(BoundFilter):

    async def check(self, message: types.Message):
        user_id = message.from_user.id
        admin_id = os.getenv("ADMIN_ID")
        admin_id_two = os.getenv("ADMIN_ID_TWO")
        if (int(user_id) == int(admin_id)) or (int(user_id) == int(admin_id_two)):
            result = True
        else:
            result = False

        return result
