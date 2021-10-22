from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.http_getter import get_golden_keys

from loader import dp


@dp.message_handler(text='/b3')
async def search_golden_key(message: types.Message):
    """Search and find new Shift Codes for Borderlands 3"""
    await message.answer('Сейчас поищем актуальные Shift коды, момент...')
    keys = await get_golden_keys()
    if keys:
        for key in keys:
            await message.answer(key)