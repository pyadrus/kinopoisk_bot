from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from database.database import get_random_movie_by_genre_and_year
from keyboards.reply.categories_btn import create_random_genre_keyboard
from system.dispatcher import dp, bot


def create_genre_random_movie_by_genre_keyboard():
    """Создайте клавиатуру с возможностью выбора жанра"""
    genres = ["комедия", "драма", "боевик", "фантастика", "ужасы", "приключения", "триллер", "фэнтези", "детектив",
              "криминал", "вестерн", "военный", "мелодрама", "мультфильм", "короткометражка", "детский", "биография",
              "история", "аниме", "семейный"]
    genre_buttons = [InlineKeyboardButton(text=genre, callback_data=f"genre_random:{genre}") for genre in genres]
    genres_markup = InlineKeyboardMarkup(row_width=3)
    genres_markup.add(*genre_buttons)
    return genres_markup


def create_year_random_movie_by_genre_keyboard():
    """Создайте клавиатуру с опциями выбора года"""
    year_ranges = ["1990-2000", "2001-2005", "2006-2010", "2011-2015", "2016-2020", "2021-2024"]

    year_buttons = [InlineKeyboardButton(text=year_range, callback_data=f"year_random:{year_range}") for year_range in
                    year_ranges]
    year_markup = InlineKeyboardMarkup(row_width=3)
    year_markup.add(*year_buttons)
    return year_markup


@dp.message_handler(lambda message: message.text == "🎬 Случайный фильм по жанру")
async def random_movie_by_genre(message: types.Message):
    chat_id = message.chat.id
    main_page_kb = create_random_genre_keyboard()
    await bot.send_message(chat_id, "🎬 Случайный фильм по жанру", reply_markup=main_page_kb)
    genres_markup = create_genre_random_movie_by_genre_keyboard()  # Клавиатура выбора жанра фильма
    await message.answer("Выберите жанр фильма:", reply_markup=genres_markup)


random_movie_by_genre_callback = CallbackData("genre_random", "genre_random")
random_movie_by_genre_user_selections = {}  # Create a dictionary to store user selections
year_random_movie_by_genre = CallbackData("year_random", "year_random")


@dp.callback_query_handler(random_movie_by_genre_callback.filter())
async def process_random_movie_by_genre_callback(query: CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    genre = callback_data["genre_random"]
    random_movie_by_genre_user_selections[chat_id] = {"genre_random": genre}
    year_markup = create_year_random_movie_by_genre_keyboard()  # Клавиатура выбора диапазона лет
    await bot.send_message(chat_id, "Выберите диапазон лет:", reply_markup=year_markup)


@dp.callback_query_handler(year_random_movie_by_genre.filter())
async def process_random_movie_by_genre(query: CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    year_range = callback_data["year_random"]
    genre = random_movie_by_genre_user_selections.get(chat_id, {}).get("genre_random", "Unknown")
    await bot.send_chat_action(chat_id, 'typing')  # Show the "bot is typing" indicator
    movie_info, poster_url = get_random_movie_by_genre_and_year(f"{genre},{year_range}")
    await bot.send_photo(chat_id, photo=poster_url, caption=movie_info)


def register_random_movie_by_genre_handler():
    dp.register_message_handler(random_movie_by_genre)
