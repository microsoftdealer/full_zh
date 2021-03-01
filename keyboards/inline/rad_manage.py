from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.rad_manage_cd import rad_remove_cd


def delete_kb(id):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Переделать', callback_data=rad_remove_cd.new(item_id=id))
    ], [InlineKeyboardButton(text='Вернуться в меню', callback_data='cancel')]])
    return kb
