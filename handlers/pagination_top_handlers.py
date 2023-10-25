import requests
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
import aiogram.utils.exceptions
from database.database import recording_movies_in_the_database, get_random_id_movies, get_movie_info
from system.dispatcher import dp, bot, API_KEY


async def get_random_movie(chat_id, api_key):
    url = 'https://api.kinopoisk.dev/v1.3/movie/random'
    headers = {'X-API-KEY': api_key}
    await bot.send_chat_action(chat_id, 'typing')  # Показываем индикатор "бот печатает" пользователю
    response = requests.get(url, headers=headers, timeout=(10, 30))
    if response.status_code == 200:
        data = response.json()
        # print(data)
        id_movies = data.get('id')
        # print(id_movies)
        name = data.get('name', 'Название фильма не найдено')
        year = data.get('year', 'Год выпуска не найден')
        rating = data.get('rating', {}).get('kp', 'Рейтинг не найден')
        description = data.get('description', 'Описание не найдено')
        genres = ', '.join([genre.get('name', '') for genre in data.get('genres', [])])
        countries = ', '.join([country.get('name', '') for country in data.get('countries', [])])
        poster_url = data.get('poster', {}).get('url', '')

        movie_info = (f'Название: {name}\n'
                      f'Год выпуска: {year}\n'
                      f'Рейтинг Кинопоиска: {rating}\n'
                      f'Жанры: {genres}\n'
                      f'Страна: {countries}\n\n'
                      f'Описание: {description}\n')
        recording_movies_in_the_database(id_movies, name, year, rating, description, genres, countries, poster_url)
        return movie_info, poster_url
    else:
        return None, None


items = {}


@dp.message_handler(lambda message: message.text == "10 cлучайных фильмов")
async def random_movie_command(message: types.Message):
    # Определите chat_id, чтобы показать индикатор "бот печатает" в нужном чате
    await message.answer("Вот 10 случайных фильмов:")
    chat_id = message.chat.id
    await bot.send_chat_action(chat_id, 'typing')  # Показываем индикатор "бот печатает"
    for i in range(10):
        try:
            random_id_movies = get_random_id_movies()
            movie_info, poster_url = get_movie_info(random_id_movies)
        except aiogram.utils.exceptions.BadRequest:
            # Handle the exception by getting a new random movie
            random_id_movies = get_random_id_movies()
            movie_info, poster_url = get_movie_info(random_id_movies)
        items[i] = [movie_info, poster_url]
    print(items)

    try:
        # Use message.answer_photo with the URL directly
        await message.answer_photo(photo=items[0][1], caption=items[0][0], reply_markup=paginator(0))
    except aiogram.utils.exceptions.BadRequest:
        # Handle the exception by informing the user that there was an issue
        await message.answer("Извините, возникла проблема с отправкой фильма. Попробуйте еще раз.")

pag_cb = CallbackData("empty", "action", "page")


def paginator(page: int = 0, total_pages: int = 10):
    buttons = [
        InlineKeyboardButton("⬅", callback_data=pag_cb.new(action="prev", page=page)),
        InlineKeyboardButton("➡", callback_data=pag_cb.new(action="next", page=page))
    ]

    # Remove the "prev" button if at the beginning
    if page == 0:
        buttons.pop(0)

    # Remove the "next" button if at the end
    if page == total_pages - 1:
        buttons.pop()

    return InlineKeyboardMarkup().row(*buttons)


@dp.callback_query_handler(pag_cb.filter(action="prev"))
async def prev_page(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) - 1 if int(callback_data["page"]) > 0 else 0
    try:
        await query.message.edit_media(InputMediaPhoto(media=items[page][1]))
        await query.message.edit_caption(caption=items[page][0], reply_markup=paginator(page))
    except IndexError:
        pass
    except KeyError:
        pass


@dp.callback_query_handler(pag_cb.filter(action="next"))
async def next_page(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) + 1
    try:
        await query.message.edit_media(InputMediaPhoto(media=items[page][1]))
        await query.message.edit_caption(caption=items[page][0], reply_markup=paginator(page))
    except aiogram.utils.exceptions.BadRequest:
        # Handle the exception by getting a new random movie
        random_id_movies = get_random_id_movies()
        movie_info, poster_url = get_movie_info(random_id_movies)
        items[page] = [movie_info, poster_url]
        await query.message.edit_media(InputMediaPhoto(media=items[page][1]))
        await query.message.edit_caption(caption=items[page][0], reply_markup=paginator(page))

    except IndexError:
        pass
    except KeyError:
        pass


@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    return True


def register_random_10_movie_command_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(random_movie_command)  # Обработчик команды /random
