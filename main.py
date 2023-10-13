from aiogram import executor
from loguru import logger

from handlers.custom_handlers.start import greeting_handler
from system.dispatcher import dp

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота


def main() -> None:
    """Запуск бота https://t.me/CineSearch24_bot"""
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as error:
        logger.exception(error)

    greeting_handler()  # Пост приветствие


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        logger.exception(e)