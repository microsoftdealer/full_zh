import datetime
import json

from aiogram import types
from aiogram.dispatcher import FSMContext
import asyncio

from aiogram.types import InputFile, ContentType

from keyboards.inline.levels import levels_kb
from keyboards.inline.menu import menu_kb, cancel_kb
from keyboards.inline.rad_manage import delete_kb
from keyboards.inline.rad_manage_cd import rad_remove_cd
from states.rad import FZH

from loader import dp
from utils.db_api.commands import new_rad, check_this_month, delete_rad
from utils.full_zh_maker import full_zh_gen
from utils.misc.analyzer import analyze


@dp.callback_query_handler(text='cancel', state='*')
async def cancel_all(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text='Возврат в меню через пару секунд...')
    await asyncio.sleep(2)
    await state.finish()
    await call.message.answer(text='Вы в главном меню.', reply_markup=menu_kb)


@dp.callback_query_handler(rad_remove_cd.filter())
async def remake(call: types.CallbackQuery):
    data = call.data
    id_to_remove = data.split(':')
    id_to_remove = id_to_remove[-1]
    await delete_rad(int(id_to_remove))
    await call.message.answer('Удалено. Жми /wheel чтобы сделать заново.')


@dp.callback_query_handler(text='wheel', state='*')
async def create_full_wheel(call: types.CallbackQuery):
    date = datetime.date.today()
    year = date.year
    month = str(date.month)
    print(year)
    print(month)
    print(type(month))
    print(type(year))

    check = await check_this_month(call.from_user.id, month, year)
    print(check)
    if check:
        await call.message.answer(text='В месяц достаточно одной штуки!\n'
                                       'Ты уже заполнял в этом месяце, вот и Колесо, кстати!')
        await call.message.answer_photo(photo=check.photo_id)
        await call.message.answer(text='Если хочешь заполнить заново - жми кнопку.', reply_markup=delete_kb(check.id))
        return
    await call.message.answer('Оки-доки, давай сделаем тебе "Колесо жизни"\n'
                              'Пока мы будем хранить его и ты даже'
                              ' сможешь посмотреть историю.\n'
                              'Если не знаешь, что это такое - прочитай краткий мануал - /help\n'
                              'Погнали!')
    await asyncio.sleep(1)
    await call.message.answer('Оцени уровень любви по шкале от 0 до 10', reply_markup=levels_kb())
    await FZH.Love.set()


@dp.message_handler(commands='wheel', state='*')
async def create_full_zh(message: types.Message, state: FSMContext):
    await state.finish()
    date = datetime.date.today()
    year = date.year
    month = str(date.month)
    check = await check_this_month(message.from_user.id, month, year)
    print(year)
    print(month)
    print(type(month))
    print(type(year))
    if check:
        await message.answer(text='В месяц достаточно одной штуки!\n'
                                  'Ты уже заполнял в этом месяце, вот и Колесо, кстати!')
        await message.answer_photo(photo=check.photo_id)
        await message.answer(text='Если хочешь заполнить заново - жми кнопку.', reply_markup=delete_kb(check.id))
        return
    await message.answer('Оки-доки, давай сделаем тебе "Колесо жизни"\n'
                         'Пока мы будем хранить его и ты даже'
                         ' сможешь посмотреть историю.\n'
                         'Если не знаешь, что это такое - прочитай краткий мануал - /help\n'
                         'Погнали!')
    await asyncio.sleep(1)
    await message.answer('💞 Оцени уровень любви по шкале от 0 до 10', reply_markup=levels_kb())
    await FZH.Love.set()


@dp.callback_query_handler(text='back', state='*')
@dp.callback_query_handler(state=FZH.Love)
@dp.callback_query_handler(state=FZH.Money)
@dp.callback_query_handler(state=FZH.Friends)
@dp.callback_query_handler(state=FZH.Health)
@dp.callback_query_handler(state=FZH.Hobby)
@dp.callback_query_handler(state=FZH.Job)
async def write_down_full_zh(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    lvl = call.data
    if lvl == 'back':
        await FZH.previous()
        await FZH.previous()
        cur_state = await state.get_state()
        if not cur_state:
            await FZH.First.set()

    cur_state = await state.get_state()
    if cur_state == 'FZH:First':
        await call.message.answer('💞 Оцени уровень любви по шкале от 0 до 10', reply_markup=levels_kb())
        await FZH.Love.set()
        return
    if cur_state == 'FZH:Love':
        await state.update_data(love=lvl) if lvl != 'back' else print('')
        await call.message.answer('💰 Оцени уровень обеспеченности по шкале от 0 до 10', reply_markup=levels_kb())
        await FZH.Money.set()
        return
    if cur_state == 'FZH:Money':
        await state.update_data(money=lvl) if lvl != 'back' else print('')
        await call.message.answer('🏐 Оцени уровень дружбы по шкале от 0 до 10', reply_markup=levels_kb())
        await FZH.Friends.set()
        return
    if cur_state == 'FZH:Friends':
        await state.update_data(friends=lvl) if lvl != 'back' else print('')
        await call.message.answer('🏥 Оцени уровень здоровья по шкале от 0 до 10', reply_markup=levels_kb())
        await FZH.Health.set()
        return
    if cur_state == 'FZH:Health':
        await state.update_data(health=lvl) if lvl != 'back' else print('')
        await call.message.answer('🎿 Оцени уровень хобби по шкале от 0 до 10', reply_markup=levels_kb())
        await FZH.Hobby.set()
        return
    if cur_state == 'FZH:Hobby':
        await state.update_data(hobby=lvl) if lvl != 'back' else print('')
        await call.message.answer('🔨 Оцени уровень работы по шкале от 0 до 10', reply_markup=levels_kb())
        await FZH.Job.set()
        return
    if cur_state == 'FZH:Job':
        await state.update_data(job=lvl)
    data = await state.get_data()
    love = data.get('love')
    money = data.get('money')
    friends = data.get('friends')
    health = data.get('health')
    hobby = data.get('hobby')
    job = data.get('job')
    df_dict = {
        'love': love,
        'money': money,
        'friends': friends,
        'health': health,
        'hobby': hobby,
        'job': job
    }
    await call.message.answer(text='Сейчас сделаем картинку, момент...')
    filename = full_zh_gen(df_dict)
    photo = InputFile(path_or_bytesio=filename)
    photo = await call.message.answer_photo(photo=photo, caption='Готово, наслаждайтесь.')
    photo_id = photo.photo[-1].file_id
    await state.finish()
    date = datetime.date.today()
    year = date.year
    month = str(date.month)
    await new_rad(call.from_user.id, year, month, photo_id, json.dumps(df_dict))
    analysis = analyze(df_dict)
    await call.message.answer(analysis)


@dp.callback_query_handler(text='cancel', state='*')
async def cancel_all(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer(text='Возврат в меню через пару секунд...')
    await asyncio.sleep(2)
    await state.finish()
    await call.message.answer(text='Вы в главном меню.', reply_markup=menu_kb)
