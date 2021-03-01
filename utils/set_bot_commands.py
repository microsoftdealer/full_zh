from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("/start", "Начало работы с ботом"),
        types.BotCommand("/history", "Посмотреть историю Колеса Жизни"),
        types.BotCommand("/wheel", "Сделать колесо жизни"),
        types.BotCommand("/donate", "Скинуться на мороженое"),
    ])
