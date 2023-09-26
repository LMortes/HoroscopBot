import asyncio


from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from .config import BOT_TOKEN
from .utils.mysql import db

load_dotenv()

async def on_startup(_):
    print('Bot started')
    loop = asyncio.get_event_loop()
    await db.connection(loop)


bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

