from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import StatesGroup, State

from database.database import get_random_movie_by_genre_year_rating_country
from system.dispatcher import dp, bot

# Создаем CallbackData для выбора страны
full_user_selection_country_callback = CallbackData("country", "country")
# Создаем CallbackData для выбора жанра
genre_callback_full_setup = CallbackData("genre", "genre")
# Создаем CallbackData для выбора года
year_callback_full_setup = CallbackData("year", "year")
# Создаем CallbackData для выбора рейтинга
top_rating_callback_full_setup = CallbackData("top_rating", "top_rating")


def create_genre_random_movie_full_setup_keyboard():
    # Создаем клавиатуру для выбора страны
    countries = ['Корея Южная', 'Аргентина', 'Испания', 'Франция', 'Нидерланды', 'Швейцария', 'Португалия', 'Беларусь',
                 'Германия', 'Италия', 'Канада', 'Япония', 'Бразилия', 'Новая Зеландия', 'Австрия', 'Колумбия', 'Китай',
                 'Дания', 'Мексика', 'ОАЭ', 'США', 'Швеция', 'Казахстан', 'ЮАР', 'Великобритания', 'Россия']
    country_buttons = [InlineKeyboardButton(text=country, callback_data=f"country:{country}") for country in countries]
    country_markup = InlineKeyboardMarkup(row_width=3)
    country_markup.add(*country_buttons)
    return country_markup


def create_genre_selection_keyboard_full_setup():
    # Создаем клавиатуру для выбора жанра
    genres = ["комедия", "драма", "боевик", "фантастика", "ужасы", "приключения", "триллер", "фэнтези", "детектив",
              "криминал", "вестерн", "военный", "мелодрама", "мультфильм", "короткометражка", "детский", "биография",
              "история", "аниме", "семейный"]
    genre_buttons = [InlineKeyboardButton(text=genre, callback_data=f"genre:{genre}") for genre in genres]
    genres_markup = InlineKeyboardMarkup(row_width=3)
    genres_markup.add(*genre_buttons)
    return genres_markup


def create_year_selection_keyboard_full_setup():
    """Создайте клавиатуру с опциями выбора года"""
    year_ranges = ["1990-2000", "2001-2005", "2006-2010", "2011-2015", "2016-2020", "2021-2024"]

    year_buttons = [InlineKeyboardButton(text=year_range, callback_data=f"year:{year_range}") for year_range in year_ranges]
    year_markup = InlineKeyboardMarkup(row_width=3)
    year_markup.add(*year_buttons)
    return year_markup


def top_create_rating_random_movie_by_rating_keyboard_full_setup():
    """Создайте клавиатуру с возможностью выбора рейтинга"""
    top_ratings = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10']

    top_rating_buttons = [InlineKeyboardButton(text=top_rating, callback_data=f"top_rating:{top_rating}") for top_rating in top_ratings]
    top_rating_markup = InlineKeyboardMarkup(row_width=3)
    top_rating_markup.add(*top_rating_buttons)
    return top_rating_markup


class GenreSelectionState(StatesGroup):
    genre_selection = State()
    country_selection = State()
    year_selection = State()
    top_rating_selection = State()


@dp.message_handler(lambda message: message.text == "🎲 5 случайных фильмов полный выбор")
async def top_random_movie_command_full_setup(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "🎲 5 случайных фильмов полный выбор")
    genres_markup_user = create_genre_selection_keyboard_full_setup()
    await message.answer("Выберите жанр фильма:", reply_markup=genres_markup_user)
    await GenreSelectionState.genre_selection.set()


@dp.callback_query_handler(genre_callback_full_setup.filter(), state=GenreSelectionState.genre_selection)
async def full_user_selection_genre(query: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(genre=callback_data["genre"])
    country_markup = create_genre_random_movie_full_setup_keyboard()
    await bot.send_message(query.message.chat.id, "Выберите страну происхождения фильма:", reply_markup=country_markup)
    await GenreSelectionState.country_selection.set()


@dp.callback_query_handler(full_user_selection_country_callback.filter(), state=GenreSelectionState.country_selection)
async def full_user_selection_country(query: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(country=callback_data["country"])
    year_markup = create_year_selection_keyboard_full_setup()
    await bot.send_message(query.message.chat.id, "Выберите диапазон лет:", reply_markup=year_markup)
    await GenreSelectionState.year_selection.set()


@dp.callback_query_handler(year_callback_full_setup.filter(), state=GenreSelectionState.year_selection)
async def full_user_selection_year(query: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(year=callback_data["year"])
    top_rating_markup = top_create_rating_random_movie_by_rating_keyboard_full_setup()
    await bot.send_message(query.message.chat.id, "Выберите рейтинг фильма:", reply_markup=top_rating_markup)
    await GenreSelectionState.top_rating_selection.set()


@dp.callback_query_handler(top_rating_callback_full_setup.filter(), state=GenreSelectionState.top_rating_selection)
async def full_user_selection_top_rating(query: CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    genre = data.get('genre', '')
    country = data.get('country', '')
    year_range = data.get('year', '')
    top_rating = callback_data["top_rating"]
    print(genre, country, year_range, top_rating)
    user_choice_message = (f"🎬 5 случайных фильмов\n\n"
                           f"🎭 Жанр: <b>{genre}</b>,\n"
                           f"📅 Год выпуска: <b>{year_range}</b>. 🎥\n"
                           f"Страна: <b>{country}</b>,\n"
                           f"Рейтинг: <b>{top_rating}</b>,\n"
                           f"<code>Если фильмы по выбранному году и жанру не найдены, то будут добавлены позже. "
                           f"Мы постоянно расширяемся и создаем свою базу, не зависимую от внешних источников.</code>")

    chat_id = query.message.chat.id
    await bot.send_message(chat_id, user_choice_message)

    await bot.send_chat_action(chat_id, 'typing')  # Показываем индикатор "бот печатает"
    try:
        for i in range(1):
            movie_info, poster_url = get_random_movie_by_genre_year_rating_country(f"{genre},{year_range},{country},{top_rating}")
            if movie_info:
                await bot.send_photo(chat_id, photo=poster_url, caption=movie_info)
            else:
                await bot.send_message(chat_id, "Фильмы по выбранным параметрам не найдены.")
    except TypeError:
        await bot.send_message(chat_id, "Фильмы по выбранным параметрам не найдены.")

    await state.finish()


def register_random_10_movie_command_handler_full_setup():
    dp.register_message_handler(top_random_movie_command_full_setup)
    dp.register_callback_query_handler(full_user_selection_genre, genre_callback_full_setup.filter())
    dp.register_callback_query_handler(full_user_selection_country, full_user_selection_country_callback.filter())
    dp.register_callback_query_handler(full_user_selection_year, year_callback_full_setup.filter())
    dp.register_callback_query_handler(full_user_selection_top_rating, top_rating_callback_full_setup.filter())
