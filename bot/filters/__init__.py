from aiogram import Dispatcher

from .is_not_admin_user import IsNotAdminUser
from .is_admin_user import IsAdminUser


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsNotAdminUser)
    dp.filters_factory.bind(IsAdminUser)
