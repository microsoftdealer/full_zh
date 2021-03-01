from aiogram.utils.callback_data import CallbackData

items_buy_cd = CallbackData('items_buy', 'item_id')
items_cancel_cd = CallbackData('items_cancel', 'item_id')
items_update_price_cd = CallbackData('items_price_mod', 'item_id')
items_update_comment_cd = CallbackData('items_comment_mod', 'item_id')
items_update_level_cd = CallbackData('items_level_mod', 'item_id')
rub_cd = CallbackData('rub', 'amount')
amount_cd = CallbackData('amount', 'threshold')