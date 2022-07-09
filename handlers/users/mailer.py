import asyncio
import datetime
import logging

import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.user_buttons import confirm_mailer_kb
from loader import dp
from utils.db_api import commands


@dp.message_handler(text='/mailer')
async def make_announce(message: Message, state: FSMContext):
    logging.info('MAILER')
    if message.from_user.id != 310729516:
        logging.info(f'User {message.from_user.username} with ID {message.from_user.id} tried to execute /mailer')
        return
    users = await commands.select_users()
    text = str([f'{user.name}' for user in users])
    await message.answer(text=f'Вы хотите создать рассылку на пользователей бота.\n'
                              f'{text}'
                              f'Введите текст для рассылки.', )
    await state.set_state('create_announce')


@dp.message_handler(state='create_announce')
async def create_announce(message: Message, state: FSMContext):
    announce_text = message.text
    await state.update_data(announce_text=announce_text)
    await state.set_state('confirm_announce')
    await message.answer(text='Почти готово.\n'
                              'Вы хотите создать рассылку с нижеприведенным текстом. Осталось подтвердить.')
    await message.answer(announce_text, reply_markup=confirm_mailer_kb)


@dp.callback_query_handler(state='confirm_announce', text='confirm_mailer')
async def confirm_announce(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    await state.finish()
    announce_text = data.get('announce_text')
    await call.answer(text='Рассылка создана! Начинаем прямо сейчас!')
    await call.message.answer(text='Сделано!\n'
                                   'По завершению рассылки уведомим отдельно.')
    users = await commands.select_users()
    counter = 0
    errors = 0
    err_bot_bl = 0
    error_bot_k = 0
    error_bot_cnf = 0
    error_bot_ud = 0
    error_bot_tapi = 0
    start_time = datetime.datetime.now()
    logging.info('List of users unprepared')
    logging.info([user.name for user in users])
    # logging.info([user.tg_id for user in users])
    # users = [user for user in users if user.tg_id == 343667544]
    # logging.info('List of users prepared')
    # logging.info([user.name for user in users])
    for user in users:
        await asyncio.sleep(.10)
        try:
            await dp.bot.send_message(chat_id=user.tg_id, text=announce_text)
            counter += 1
        except aiogram.exceptions.RetryAfter as err:
            await asyncio.sleep(err.timeout)
            await dp.bot.send_message(chat_id=user.tg_id, text=announce_text)
            counter += 1
        except aiogram.exceptions.BotBlocked as err:
            errors += 1
            err_bot_bl += 1
            logging.info(f'Exception {err} has been occurred when sending to {user.name} with tg_id {user.tg_id}')
            await asyncio.sleep(1)
        except aiogram.exceptions.BotKicked as err:
            errors += 1
            error_bot_k += 1
            logging.info(f'Exception {err} has been occurred when sending to {user.name} with tg_id {user.tg_id}')
            await asyncio.sleep(1)
        except aiogram.exceptions.ChatNotFound as err:
            errors += 1
            error_bot_cnf += 1
            logging.info(f'Exception {err} has been occurred when sending to {user.name} with tg_id {user.tg_id}')
            await asyncio.sleep(1)
        except aiogram.exceptions.UserDeactivated as err:
            errors += 1
            error_bot_ud += 1
            logging.info(f'Exception {err} has been occurred when sending to {user.name} with tg_id {user.tg_id}')
            await asyncio.sleep(1)
        except aiogram.exceptions.TelegramAPIError as err:
            errors += 1
            error_bot_tapi += 1
            logging.info(f'Exception {err} has been occurred when sending to {user.name} with tg_id {user.tg_id}')
            await asyncio.sleep(1)
    finish_time = datetime.datetime.now()
    delta = finish_time - start_time
    seconds_overall = delta.seconds
    minutes = seconds_overall // 60
    seconds = seconds_overall % 60
    await call.message.answer(f'Рассылка завершена за {minutes} минут {seconds} секунд.\n'
                              f'Всего отправлено {counter} сообщений.\n'
                              f'Ошибок при отправке - {errors}\n'
                              f'Из них:\n'
                              f'Пользователь заблокировал бота (STOPPED) - {err_bot_bl}\n'
                              f'Бот удален из группы - {error_bot_k}\n'
                              f'Несуществующий Chat_id - {error_bot_cnf}\n'
                              f'Пользователь деактивировал аккаунт - {error_bot_ud}\n'
                              f'Ошибка API Telegram - {error_bot_tapi}')
