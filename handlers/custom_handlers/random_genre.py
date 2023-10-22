import requests
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, CallbackQuery
from aiogram.utils.callback_data import CallbackData

import random
from database.database import recording_movies_in_the_database
from system.dispatcher import dp, bot, API_KEY


def get_random_movie_genres(genres, year_range):
    headers = {'X-API-KEY': API_KEY}
    response = requests.get('https://api.kinopoisk.dev/v1.3/movie',
                            params={"genres.name": genres, "limit": 1, "page": 1, "year": year_range},
                            headers=headers)
    if response.status_code == 200:
        movies = response.json()
        print(movies)
        total_pages = movies["total"] // movies["limit"] + (1 if movies["total"] % movies["limit"] > 0 else 0)
        random_page = random.randint(1, total_pages)
        response = requests.get('https://api.kinopoisk.dev/v1/movie',
                                params={"genres.name": genres, "limit": 1, "page": random_page, "year": year_range},
                                headers=headers)
        if response.status_code == 200:
            movie = response.json()['docs'][0]  # Get the first movie from the response
            print(movie)
            id_movies = movie.get('id')
            print(id_movies)
            name = movie.get('names', [{}])[0].get('name', 'Название фильма не найдено')
            year = movie.get('year', 'Год выпуска не найден')
            rating = movie['rating'].get('kp', 'Рейтинг не найден')
            description = movie.get('description', 'Описание отсутствует')  # Handle missing 'description' key
            genres = ', '.join([genre.get('name', '') for genre in movie.get('genres', [])])
            countries = ', '.join([country.get('name', '') for country in movie.get('countries', [])])

            poster = movie.get('poster', {})
            poster_url = poster.get('url', '') if poster else ''  # Handle missing 'poster' key

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
    else:
        return None, None


@dp.message_handler(lambda message: message.text == "Случайные фильм по жанрам")
async def choose_genre(message: types.Message):
    # Определите chat_id, чтобы показать индикатор "бот печатает" в нужном чате
    chat_id = message.chat.id
    # Показываем индикатор "бот печатает"
    await bot.send_chat_action(chat_id, 'typing')
    # Создайте список доступных жанров
    genres = ["комедия", "драма", "боевик", "фантастика", "ужасы", "приключения", "триллер", "фэнтези", "детектив",
              "криминал", "вестерн", "военный", "мелодрама", "мультфильм", "короткометражка", "детский", "биография",
              "история", "аниме", "семейный"]
    # Создайте список кнопок для клавиатуры
    genre_buttons = [InlineKeyboardButton(text=genre, callback_data=f"genre:{genre}") for genre in genres]
    # Создайте клавиатуру
    genres_markup = InlineKeyboardMarkup(row_width=3)
    genres_markup.add(*genre_buttons)
    # Отправляем сообщение с предложением выбрать жанр
    print(genres_markup)
    await message.answer("Выберите жанр фильма:", reply_markup=genres_markup)


genre_callback = CallbackData("genre", "genre")
year_callback = CallbackData("year", "year")
# Create a dictionary to store user selections
user_selections = {}


@dp.callback_query_handler(genre_callback.filter())
async def process_genre_callback(query: CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    genre = callback_data["genre"]
    # Save the selected genre in the user's state
    user_selections[chat_id] = {"genre": genre}
    # Trigger year selection
    await choose_year(query)


async def choose_year(query: CallbackQuery):
    chat_id = query.message.chat.id
    year_ranges = ["1990-1995", "1996-2000", "2001-2005", "2006-2010", "2011-2015", "2016-2020", "2021-2023"]
    year_markup = InlineKeyboardMarkup(row_width=3)

    # Use the correct key 'year' in callback_data.new
    year_buttons = [InlineKeyboardButton(text=year_range, callback_data=year_callback.new(year=year_range)) for
                    year_range in year_ranges]
    year_markup.add(*year_buttons)
    await bot.send_message(chat_id, "Выберите диапазон лет:", reply_markup=year_markup)


@dp.callback_query_handler(year_callback.filter())
async def process_year_callback(query: CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    year_range = callback_data["year"]
    genre = user_selections.get(chat_id, {}).get("genre", "Unknown")
    # Use the selected genre and year range to fetch a random movie
    movie_info, poster_url = get_random_movie_genres(genre, year_range)

    if movie_info:
        if poster_url:
            await bot.send_photo(chat_id, photo=poster_url, caption=movie_info)
        else:
            await bot.send_message(chat_id, movie_info, parse_mode=ParseMode.HTML)
    else:
        await bot.send_message(chat_id, "Извините, не удалось получить информацию о фильме.")


def register_random_genre_movie_command_handler():
    dp.register_message_handler(choose_genre)
    dp.register_callback_query_handler(process_genre_callback)
    dp.register_callback_query_handler(process_year_callback)
