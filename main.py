from aiogram import executor
from loguru import logger

from handlers.pagination_random_genre import register_random_10_movie_command_handler_genres_1
from handlers.pagination_top_handlers import register_random_10_movie_command_handler
from handlers.random import register_random_movie_command_handler
from handlers.random_genre import register_random_movie_by_genre_handler
from handlers.start import register_greeting_handler
from system.dispatcher import dp

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота


def main() -> None:
    """Запуск бота https://t.me/CineSearch24_bot"""
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as error:
        logger.exception(error)

    register_greeting_handler()  # Пост приветствие, команда /start
    register_random_movie_command_handler()  # Рандомный фильм
    register_random_10_movie_command_handler()  # 10 случайных фильмов
    register_random_10_movie_command_handler_genres_1()
    register_random_movie_by_genre_handler()


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        logger.exception(e)
