from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.date_mover_cd import mover_cd

menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🎡 Построить колесо жизни!', callback_data='wheel')
    ],
    [
        InlineKeyboardButton(text='📜 Ваша история', callback_data='history')
    ],
    [
        InlineKeyboardButton(text='💰 Помочь проекту', callback_data='donate')
    ]
])

cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Вернуться в меню.', callback_data='cancel')
    ]
])

month_dict = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}


def history_kb(user_id, month, year):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='◀', callback_data=mover_cd.new(month=month, year=year - 1)),
            InlineKeyboardButton(text='⬅', callback_data=mover_cd.new(month=month - 1, year=year)),
            InlineKeyboardButton(text='➡', callback_data=mover_cd.new(month=month + 1, year=year)),
            InlineKeyboardButton(text='▶', callback_data=mover_cd.new(month=month, year=year + 1)),
        ],
        [
            InlineKeyboardButton(text=f'{month_dict[month]} {year}', callback_data='pussy')
        ],
        [
            InlineKeyboardButton(text='Описание', callback_data='description')
        ],
        [
            InlineKeyboardButton(text='Вернуться в меню', callback_data='cancel')
        ]
    ])
    return kb


photo_set = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Установить фото', callback_data='set_photo')
    ]
])
