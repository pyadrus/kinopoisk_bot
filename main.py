from aiogram import executor
from loguru import logger

from handlers.admin_handlers import register_admin_handler
from handlers.pagination_random.pagination_menu_random import pagination_register_menu_random_handler
from handlers.pagination_random.pagination_random_country import register_random_movie_country
from handlers.pagination_random.pagination_random_full_setup import register_random_5_movie_command_handler_full_setup
from handlers.random.menu_random import register_menu_random_handler
from handlers.random.random_full_setup import register_random_10_movie_command_handler_full_setup
from handlers.pagination_random.pagination_random_genre import register_random_10_movie_command_handler_genres_1
from handlers.pagination_random.pagination_random_rating import register_random_movie_rating
from handlers.pagination_random.pagination_top_handlers import register_random_10_movie_command_handler
from handlers.random.random import register_random_movie_command_handler
from handlers.random.random_country import register_random_country_handler
from handlers.random.random_genre import register_random_movie_by_genre_handler
from handlers.random.random_rating import register_random_rating_handler
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
    register_random_country_handler()  # Рандомный фильм по стране происхождению
    register_random_rating_handler()  # Рандомный фильм по рейтингу
    register_random_movie_country()
    register_random_movie_rating()
    register_random_10_movie_command_handler_full_setup()  # рандомный фильм полный выбор пользователя
    register_random_5_movie_command_handler_full_setup()  # 5 рандомных фильмов полный выбор пользователя
    register_menu_random_handler()
    pagination_register_menu_random_handler()
    register_admin_handler()  # Проверка на подписку


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        logger.exception(e)
