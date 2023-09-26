from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Статистика'),
            KeyboardButton(text='Обяз. Подписка'),
        ],
        [
            KeyboardButton(text='Рассылка'),
            KeyboardButton(text='Рефералы'),
        ]
    ],
    resize_keyboard=True
)


main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='💟 Совместимость'),
            KeyboardButton(text='🔮 Гороскоп'),
        ],
        [
            KeyboardButton(text='🟣 Магия чисел'),
            KeyboardButton(text='🀄️ Карты таро'),
        ],
        [
            KeyboardButton(text='🏵 Восточный гороскоп'),
        ],
        [
            KeyboardButton(text='🪬 Личные консультации'),
        ],
    ],
    resize_keyboard=True
)






horo_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='♈️ Овен'),
            KeyboardButton(text='♉️ Телец'),
            KeyboardButton(text='♊️ Близнецы'),
        ],
        [
            KeyboardButton(text='♋️ Рак'),
            KeyboardButton(text='♌️ Лев'),
            KeyboardButton(text='♍️ Дева'),
        ],
        [
            KeyboardButton(text='♎️ Весы'),
            KeyboardButton(text='♏️ Скорпион'),
            KeyboardButton(text='♐️ Стрелец'),
        ],
        [
            KeyboardButton(text='♑️ Козерог'),
            KeyboardButton(text='♒️ Водолей'),
            KeyboardButton(text='♓️ Рыбы'),
        ],
    ]
)

cons_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔮 Персональный гороскоп на 2023 год'),
        ],
        [
            KeyboardButton(text='❤️‍🔥 Личный код любви и изобилия'),
        ],
        [
            KeyboardButton(text='👩‍❤️‍👨 Личный код совместимости партнеров'),
        ],
        [
            KeyboardButton(text='🀄️ Расклад натальной карты'),
        ],
        [
            KeyboardButton(text='🏆 Число жизненного пути'),
            KeyboardButton(text='💫 Число Судьбы (Имени)'),
        ],
    ],
    resize_keyboard=True,
)

goto_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🏠 Главное меню'),
        ],
    ],
    resize_keyboard=True,
)