from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.user_buttons import donate_kb, paid_kb, select_sum
from keyboards.inline.user_buttons_cd import rub_cd, amount_cd
from loader import dp
from data import config

from utils.db_api import commands
from utils.misc.kiwi import Payment, NoPaymentFound, NotEnoughMoney


@dp.callback_query_handler(text='donate')
async def choose_item(call: CallbackQuery):
    await call.message.edit_text(text='Тут можно помочь автору на серверы и мороженое,\n'
                                      'выберите сумму:', reply_markup=donate_kb)


@dp.callback_query_handler(rub_cd.filter())
async def need_to_pay(call: CallbackQuery, callback_data: dict):
    amount = callback_data['amount']
    amount = int(amount)
    if amount == 0:
        await call.message.edit_text(text='Выберите произвольную сумму, '
                                          'или введите ее в сообщении:', reply_markup=select_sum())
        return
    payment = Payment(amount=amount)
    payment.create()
    await call.message.edit_text(text='Выберите способ оплаты:', reply_markup=paid_kb(payment.invoice))


@dp.callback_query_handler(amount_cd.filter())
async def new_sum_generate(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    amount = state_data.get('sum')
    data = call.data
    if not amount:
        amount = 0
        await state.update_data(sum=amount)
    threshold = int(data.split(':')[-1])
    threshold = amount + threshold
    if threshold <= 0:
        threshold = 1
        await state.update_data(sum=threshold)
        await call.message.edit_text(text='Выберите произвольную сумму, '
                                          'или введите ее в сообщении:', reply_markup=select_sum(threshold))
    await state.update_data(sum=threshold)
    await call.message.edit_text(text='Выберите произвольную сумму, '
                                      'или введите ее в сообщении:', reply_markup=select_sum(threshold))
