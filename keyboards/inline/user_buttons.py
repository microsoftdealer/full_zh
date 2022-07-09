from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.user_buttons_cd import items_buy_cd, items_cancel_cd, items_update_price_cd, \
    items_update_comment_cd, items_update_level_cd, rub_cd, amount_cd

user_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='📃Проверить список покупок', callback_data='show_items')
    ],
    [
        InlineKeyboardButton(text='➕Добавить покупку', callback_data='item_add')
    ]
])

level_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='♨Критично', callback_data='show_critical')
    ],
    [
        InlineKeyboardButton(text='❗Важно', callback_data='show_important')
    ],
    [
        InlineKeyboardButton(text='😎Обычные покупки', callback_data='show_common')
    ],
    [
        InlineKeyboardButton(text='💵Отложить деньги и купить', callback_data='show_uncommon')
    ],
    [
        InlineKeyboardButton(text='📜Полный список', callback_data='show_all')
    ]
])


def item_kb(item_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='✅️Куплено!', callback_data=items_buy_cd.new(item_id=item_id)),
            InlineKeyboardButton(text='❌Отказано!', callback_data=items_cancel_cd.new(item_id=item_id))
        ],
        [
            InlineKeyboardButton(text='💲Изменить цену', callback_data=items_update_price_cd.new(item_id=item_id))
        ],
        [
            InlineKeyboardButton(text='🗨Изменить комментарий',
                                 callback_data=items_update_comment_cd.new(item_id=item_id))
        ],
        [
            InlineKeyboardButton(text='📑Изменить категорию', callback_data=items_update_level_cd.new(item_id=item_id))
        ]
    ])
    return kb


cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='📜Вернуться в основное меню', callback_data='cancel')
    ]
])

level_set_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='♨Критично', callback_data='critical')
    ],
    [
        InlineKeyboardButton(text='❗Важно', callback_data='important')
    ],
    [
        InlineKeyboardButton(text='😎Обычные покупки', callback_data='common')
    ],
    [
        InlineKeyboardButton(text='💵Отложить деньги и купить', callback_data='uncommon')
    ]
])

confirm_mailer_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Отлично, рассылаем', callback_data='confirm_mailer'),
        InlineKeyboardButton(text='Вернуться в меню', callback_data='cancel')
    ]
])

confirm_buy_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='✅️Да, куплено!', callback_data='buy_item'),
        InlineKeyboardButton(text='❌Не куплено.', callback_data='cancel')
    ]
])

confirm_cancel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='✅Да, отказ!', callback_data='cancel_item'),
        InlineKeyboardButton(text='❌Не, оставьте.', callback_data='cancel')
    ]
])

confirm_modify_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='✔️Да, меняем!', callback_data='modify_item'),
        InlineKeyboardButton(text='❌Не, оставьте.', callback_data='cancel')
    ]
])

donate_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='20 RUR', callback_data=rub_cd.new(amount='20')),
            InlineKeyboardButton(text='40 RUR', callback_data=rub_cd.new(amount='40')),
            InlineKeyboardButton(text='80 RUR', callback_data=rub_cd.new(amount='80'))
        ],
        [
            InlineKeyboardButton(text='160 RUR', callback_data=rub_cd.new(amount='160')),
            InlineKeyboardButton(text='320 RUR', callback_data=rub_cd.new(amount='320')),
            InlineKeyboardButton(text='640 RUR', callback_data=rub_cd.new(amount='640'))
        ],
        [
            InlineKeyboardButton(text='1280 RUR', callback_data=rub_cd.new(amount='1280')),
            InlineKeyboardButton(text='2560 RUR', callback_data=rub_cd.new(amount='2560')),
            InlineKeyboardButton(text='5120 RUR', callback_data=rub_cd.new(amount='5120'))
        ],
        [
            InlineKeyboardButton(text='Другая сумма', callback_data=rub_cd.new(amount='0'))
        ]
    ]
)


def paid_kb(url):
    paid_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Оплата Visa/Mastercard/QIWI',
                    callback_data='card_payment',
                    url=url
                )
            ],
            [
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data="cancel")
            ],
        ]
    )
    return paid_keyboard


def select_sum(threshold=1):
    sum_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='-1к', callback_data=amount_cd.new(threshold='-1000')),
            InlineKeyboardButton(text='-100', callback_data=amount_cd.new(threshold='-100')),
            InlineKeyboardButton(text='-10', callback_data=amount_cd.new(threshold='-10')),
            InlineKeyboardButton(text='+10', callback_data=amount_cd.new(threshold='10')),
            InlineKeyboardButton(text='+100', callback_data=amount_cd.new(threshold='100')),
            InlineKeyboardButton(text='+1к', callback_data=amount_cd.new(threshold='1000'))
        ],
        [
            InlineKeyboardButton(text=f'{threshold} RUR', callback_data=rub_cd.new(amount=threshold))
        ]
    ])
    return sum_kb


