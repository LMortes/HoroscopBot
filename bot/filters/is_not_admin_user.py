import os
from dotenv import load_dotenv
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

load_dotenv()


class IsNotAdminUser(BoundFilter):

    async def check(self, message: types.Message):
        user_id = message.from_user.id
        admin_id = os.getenv("ADMIN_ID")
        if int(user_id) == int(admin_id):
            result = False
        else:
            result = True

        return result
