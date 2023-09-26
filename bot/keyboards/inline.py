from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.mysql import db


async def compatibility_keyboard():
    ikb_compatibility = InlineKeyboardMarkup(row_width=3)

    ikb_aries_button = InlineKeyboardButton(text='♈️ Овен', callback_data='comp_aries')
    ikb_taurus_button = InlineKeyboardButton(text='♉️ Телец', callback_data='comp_taurus')
    ikb_twins_button = InlineKeyboardButton(text='♊️ Близнецы', callback_data='comp_twins')
    ikb_cancer_button = InlineKeyboardButton(text='♋️ Рак', callback_data='comp_cancer')
    ikb_leo_button = InlineKeyboardButton(text='♌️ Лев', callback_data='comp_leo')
    ikb_maiden_button = InlineKeyboardButton(text='♍️ Дева', callback_data='comp_maiden')
    ikb_libra_button = InlineKeyboardButton(text='♎️ Весы', callback_data='comp_libra')
    ikb_scorpio_button = InlineKeyboardButton(text='♏️ Скорпион', callback_data='comp_scorpio')
    ikb_sagittarius_button = InlineKeyboardButton(text='♐️ Стрелец', callback_data='comp_sagittarius')
    ikb_capricorn_button = InlineKeyboardButton(text='♑️ Козерог', callback_data='comp_capricorn')
    ikb_aquarius_button = InlineKeyboardButton(text='♒️ Водолей', callback_data='comp_aquarius')
    ikb_pisces_button = InlineKeyboardButton(text='♓️ Рыбы', callback_data='comp_pisces')

    ikb_compatibility\
    .add(ikb_aries_button, ikb_taurus_button, ikb_twins_button)\
    .add(ikb_cancer_button, ikb_leo_button, ikb_maiden_button) \
    .add(ikb_libra_button, ikb_scorpio_button, ikb_sagittarius_button) \
    .add(ikb_capricorn_button, ikb_aquarius_button, ikb_pisces_button)

    return ikb_compatibility


async def ikb_eastern():
    ikb_eastern = InlineKeyboardMarkup(row_width=4)

    ikb_mouse_button = InlineKeyboardButton(text='Мышь', callback_data='eastern_mouse')
    ikb_bull_button = InlineKeyboardButton(text='Бык', callback_data='eastern_bull')
    ikb_tiger_button = InlineKeyboardButton(text='Тигр', callback_data='eastern_tiger')
    ikb_rabbit_button = InlineKeyboardButton(text='Кролик', callback_data='eastern_rabbit')
    ikb_dragon_button = InlineKeyboardButton(text='Дракон', callback_data='eastern_dragon')
    ikb_snake_button = InlineKeyboardButton(text='Змея', callback_data='eastern_snake')
    ikb_horse_button = InlineKeyboardButton(text='Лошадь', callback_data='eastern_horse')
    ikb_goat_button = InlineKeyboardButton(text='Коза', callback_data='eastern_goat')
    ikb_monkey_button = InlineKeyboardButton(text='Обезьяна', callback_data='eastern_monkey')
    ikb_cock_button = InlineKeyboardButton(text='Петух', callback_data='eastern_cock')
    ikb_dog_button = InlineKeyboardButton(text='Собака', callback_data='eastern_dog')
    ikb_pig_button = InlineKeyboardButton(text='Свинья', callback_data='eastern_pig')

    ikb_eastern\
    .add(ikb_mouse_button, ikb_bull_button, ikb_tiger_button, ikb_rabbit_button)\
    .add(ikb_dragon_button, ikb_snake_button, ikb_horse_button, ikb_goat_button)\
    .add(ikb_monkey_button, ikb_cock_button, ikb_dog_button, ikb_pig_button)

    return ikb_eastern


async def magic_numbers_ikb(random_numbers):
    ikb_magic_numbers = InlineKeyboardMarkup(row_width=5)

    for number in random_numbers:
        ikb_magic_button = InlineKeyboardButton(text=f'{number} 🔮', callback_data='magic_number')
        ikb_magic_numbers.insert(ikb_magic_button)

    return ikb_magic_numbers


async def taro_ikb(numbers):
    ikb_taro = InlineKeyboardMarkup(row_width=4)

    for number in numbers:
        ikb_taro_button = InlineKeyboardButton(text=f'{number} 💫', callback_data='taro')
        ikb_taro.insert(ikb_taro_button)

    return ikb_taro

async def ikb_horoscop_calendar():
    ikb_horoscop_calendar = InlineKeyboardMarkup(row_width=3)

    ikb_horo_cal_button_today = InlineKeyboardButton(text='На сегодня', callback_data='horo_cal_today')
    ikb_horo_cal_button_tomorrow = InlineKeyboardButton(text='На завтра', callback_data='horo_cal_tomorrow')
    ikb_horo_cal_button_week = InlineKeyboardButton(text='На неделю', callback_data='horo_cal_week')
    ikb_horo_cal_button_month = InlineKeyboardButton(text='На месяц', callback_data='horo_cal_month')
    ikb_horo_cal_button_year = InlineKeyboardButton(text='На год', callback_data='horo_cal_year')

    ikb_horoscop_calendar.add(ikb_horo_cal_button_today, ikb_horo_cal_button_tomorrow, ikb_horo_cal_button_week).add(ikb_horo_cal_button_month, ikb_horo_cal_button_year)

    return ikb_horoscop_calendar

# --------------------------------- admin mailing -----------------------------------
# Добавляем или нет кнопки
ikb_admin_sender = InlineKeyboardMarkup(row_width=1)

ikb_admin_sender_button_add = InlineKeyboardButton(text='Добавляем', callback_data='button_sender_add')
ikb_admin_sender_button_no = InlineKeyboardButton(text='Давай-ка без кнопок сегодня', callback_data='button_sender_no')

ikb_admin_sender.add(ikb_admin_sender_button_add).add(ikb_admin_sender_button_no)

# Сколько кнопок добавляем к рассылке

async def admin_sender_count_buttons():
    ikb_admin_sender_count_buttons = InlineKeyboardMarkup(row_width=5)

    for i in range(1, 11):
        ikb_admin_sender_count_button = InlineKeyboardButton(text=f'{i}', callback_data=f'count_sender_buttons_{i}')
        ikb_admin_sender_count_buttons.insert(ikb_admin_sender_count_button)
    return ikb_admin_sender_count_buttons

async def add_keyboard_for_sender(count_buttons, text_arr):
    added_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = text_arr.split('||')
    if len(buttons) != count_buttons:
        return False
    text_button = []
    url_button = []
    for buttons in buttons:
        text, url = buttons.split('|')
        text_button.append(text)
        url_button.append(url)
    for text, url in zip(text_button, url_button):
        add_button = InlineKeyboardButton(text=text, url=url)
        added_keyboard.insert(add_button)
    return added_keyboard

# ---------------------------------- ADMIN OP ----------------------------------------

ikb_admin_channels_op_edit = InlineKeyboardMarkup(row_width=2)

ikb_admin_channels_op_button_add = InlineKeyboardButton(text='Добавить', callback_data='admin_chan_op_add')
ikb_admin_channels_op_button_delete = InlineKeyboardButton(text='Удалить', callback_data='admin_chan_op_delete')

ikb_admin_channels_op_edit.row(ikb_admin_channels_op_button_add, ikb_admin_channels_op_button_delete)


async def admin_delete_channels_op_keyboard(channels):
    ikb_admin_channels_op = InlineKeyboardMarkup(row_width=5)

    for channel in channels:
        add_channel_button = InlineKeyboardButton(text=f'{channel[1]}', callback_data=f'channel_op_delete_{channel[0]}')
        ikb_admin_channels_op.insert(add_channel_button)

    return ikb_admin_channels_op


# ----------------------------- ADMIN REFERAL ------------------------------------------
async def ikb_referals_links():
    ikb_referal_links = InlineKeyboardMarkup(row_width=1)

    ref_links_info = await db.get_referal_link_info()
    if ref_links_info == False:
        return None

    for link in ref_links_info:
        ikb_ref_button = InlineKeyboardButton(text=f'{link[1]}', callback_data=f'referal_link_{link[0]}')
        ikb_referal_links.add(ikb_ref_button)

    return ikb_referal_links





















