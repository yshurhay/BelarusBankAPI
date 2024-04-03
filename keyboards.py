from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Получить новости'),
            KeyboardButton(text='Количество символов')
        ],
        [
            KeyboardButton(text='Самый длинный текст'),
            KeyboardButton(text='Самый длинный заголовок')
        ],
        [
            KeyboardButton(text='Новости в чётные дни'),
            KeyboardButton(text='Новости в нечётные дни')
        ]
    ],
    resize_keyboard=True
)
