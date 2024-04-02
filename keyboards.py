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
        ]
    ],
    resize_keyboard=True
)
