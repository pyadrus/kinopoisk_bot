from aiogram import executor
from loguru import logger

from handlers.custom_handlers.help import register_hello_replier_handler
from handlers.custom_handlers.random import register_random_movie_command_handler
from handlers.custom_handlers.random_genre import register_random_genre_movie_command_handler
from handlers.custom_handlers.start import register_greeting_handler
from system.dispatcher import dp

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота


def main() -> None:
    """Запуск бота https://t.me/CineSearch24_bot"""
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as error:
        logger.exception(error)

    register_greeting_handler()  # Пост приветствие, команда /start
    register_hello_replier_handler()  # Команда /help
    register_random_movie_command_handler()  # Рандомный фильм
    register_random_genre_movie_command_handler()  # Рандомный фильм по жанру


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        logger.exception(e)
