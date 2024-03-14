import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import handler_user
from config import config
from bot_logic import set_menu_commands


async def main():
    # Инициализация бота
    storage: MemoryStorage = MemoryStorage()
    bot: Bot = Bot(token=config.BOT_TOKEN)
    dp: Dispatcher = Dispatcher(storage=storage)

    # создать команды в меню
    await set_menu_commands(bot=bot)

    # Регистрируем роутеры в диспетчере
    dp.include_router(handler_user.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=False)  # False > бот ответит на апдейты, присланные за время откл
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
