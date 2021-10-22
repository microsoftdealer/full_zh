import json

from aiogram import types
from aiogram.dispatcher import FSMContext

import datetime

from aiogram.types import InputMediaPhoto, InputFile

from keyboards.inline.date_mover_cd import mover_cd
from keyboards.inline.menu import history_kb
from loader import dp
from utils.db_api.commands import check_this_month
from utils.misc.analyzer import analyze

def_photo = 'AgACAgIAAxkDAAID-GA9Me0H7GQ23szEP-Ckvz6UurI7AAJqszEbtevxSUBmTbdfHgqg-6Ujmy4AAwEAAwIAA3gAAwm_AwABHgQ'


@dp.message_handler(text='/history', state='*')
async def history(message: types.Message, state: FSMContext):
    await state.finish()
    date = datetime.date.today()
    month = date.month
    year = date.year
    rad = await check_this_month(message.from_user.id, month, year)
    df_dict = json.loads(rad.state)
    if rad:
        await message.answer_photo(rad.photo_id, reply_markup=history_kb(message.from_user.id, month, year))
        text = analyze(df_dict)
        await state.update_data(text=text)
    else:
        await message.answer(text='В этом месяце ничего нет.',
                             reply_markup=history_kb(message.from_user.id, month, year))


@dp.callback_query_handler(text='history', state='*')
async def history(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    date = datetime.date.today()
    month = date.month
    year = date.year
    rad = await check_this_month(call.from_user.id, month, year)
    if rad:
        print(rad.state)
        df_dict = json.loads(rad.state)
        await call.message.answer_photo(rad.photo_id, reply_markup=history_kb(call.from_user.id, month, year))
        text = analyze(df_dict)
        await state.update_data(text=text)
    else:
        await call.message.answer_photo(photo=def_photo, caption='В этом месяце ничего нет.',
                                        reply_markup=history_kb(call.from_user.id, month, year))


@dp.callback_query_handler(mover_cd.filter())
async def move_history(call: types.CallbackQuery, state: FSMContext):
    # await call.message.delete()
    state_data = await state.get_data()
    msg_to_remove = state_data.get('msg')
    data = call.data
    month = int(data.split(':')[-2])
    year = int(data.split(':')[-1])
    if month == 0:
        month = 12
        year -= 1
    if month == 13:
        month = 1
        year += 1
    rad = await check_this_month(call.from_user.id, month, year)
    if rad:
        df_dict = json.loads(rad.state)
        await call.message.edit_media(InputMediaPhoto(media=rad.photo_id),
                                      reply_markup=history_kb(call.from_user.id, month, year))
        # await call.message.answer_photo(rad.photo_id, reply_markup=history_kb(call.from_user.id, month, year))
        text = analyze(df_dict)
        await state.update_data(text=text)
    else:
        text = 'Тут у Вас ничего не записано!'
        await state.update_data(text=text)
        await call.message.edit_media(InputMediaPhoto(
            media=def_photo),
            reply_markup=history_kb(call.from_user.id, month, year))
    if msg_to_remove:
        chat_id = call.message.chat.id
        await dp.bot.delete_message(chat_id=chat_id, message_id=msg_to_remove)


@dp.callback_query_handler(text='description')
async def get_description(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    msg = await call.message.answer(text=text)
    await state.update_data(msg=msg.message_id)
