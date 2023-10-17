import requests
from aiogram.dispatcher.filters import state

import random
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from system.dispatcher import dp, bot

# Замените 'YOUR_API_KEY' на ваш реальный ключ API
API_KEY = '5M8YYRN-5T3MTDZ-MES7BD1-W54W07X'


async def get_random_movie(chat_id, api_key):
    url = 'https://api.kinopoisk.dev/v1.3/movie/random'
    headers = {'X-API-KEY': api_key}

    # Показываем индикатор "бот печатает" пользователю
    await bot.send_chat_action(chat_id, 'typing')

    response = requests.get(url, headers=headers, timeout=(10, 30))

    if response.status_code == 200:
        data = response.json()
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
        return movie_info, poster_url
    else:
        return None, None


@dp.message_handler(lambda message: message.text == "Случайные фильм")
async def random_movie_command(message: types.Message):
    # Определите chat_id, чтобы показать индикатор "бот печатает" в нужном чате
    chat_id = message.chat.id
    # Показываем индикатор "бот печатает"
    await bot.send_chat_action(chat_id, 'typing')
    # Получаем информацию о случайном фильме
    movie_info, poster_url = await get_random_movie(chat_id, API_KEY)
    if movie_info:
        if poster_url:
            await message.answer_photo(poster_url, caption=movie_info)
    else:
        await message.answer("Не удалось получить данные о фильме. Попробуйте ещё раз позже.")


def get_random_movie_genres(genres, year_range):
    headers = {'X-API-KEY': "GJ616KK-DPC4PAH-NQVE0SS-K7Y563C"}
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
              "криминал", "вестерн", "военный", "мелодрама"]
    # Создайте список кнопок для клавиатуры
    genre_buttons = [InlineKeyboardButton(text=genre, callback_data=f"genre:{genre}") for genre in genres]
    # Создайте клавиатуру
    genres_markup = InlineKeyboardMarkup(row_width=3)
    genres_markup.add(*genre_buttons)
    # Отправляем сообщение с предложением выбрать жанр
    print(genres_markup)
    await message.answer("Выберите жанр фильма:", reply_markup=genres_markup)


genre_callback = CallbackData("genre", "genre")


@dp.callback_query_handler(genre_callback.filter())
async def process_genre_callback(query: CallbackQuery, callback_data: dict):
    genre = callback_data["genre"]
    chat_id = query.message.chat.id
    year_range = "1992-2023"  # Измените годовой диапазон по вашему выбору
    movie_info, poster_url = get_random_movie_genres(genre, year_range)
    if movie_info:
        # Отправляем информацию о фильме
        if poster_url:
            await bot.send_photo(chat_id, photo=poster_url, caption=movie_info)
        else:
            await bot.send_message(chat_id, movie_info, parse_mode=ParseMode.HTML)
    else:
        await bot.send_message(chat_id, "Извините, не удалось получить информацию о фильме.")


def register_random_movie_command_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(random_movie_command)  # Обработчик команды /random
    dp.register_message_handler(choose_genre)  # Обработчик команды /random
