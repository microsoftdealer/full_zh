from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline import menu
from loader import dp
from utils.db_api.commands import add_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=menu.menu_kb)
    await add_user(message.from_user.id, message.from_user.full_name)

