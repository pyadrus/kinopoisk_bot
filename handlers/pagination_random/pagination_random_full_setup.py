from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.callback_data import CallbackData
import aiogram.utils.exceptions
from loguru import logger

from database.database import get_random_movie_by_genre_year_rating_country
from keyboards.reply.categories_btn import five_films_complete_selection_keyboard
from system.dispatcher import dp, bot

# Создаем CallbackData для выбора страны
pagination_full_user_selection_country_callback = CallbackData("country", "country")
# Создаем CallbackData для выбора жанра
pagination_genre_callback_full_setup = CallbackData("genre", "genre")
# Создаем CallbackData для выбора года
pagination_year_callback_full_setup = CallbackData("year", "year")
# Создаем CallbackData для выбора рейтинга
pagination_top_rating_callback_full_setup = CallbackData("top_rating", "top_rating")


def pagination_create_genre_random_movie_full_setup_keyboard():
    # Создаем клавиатуру для выбора страны
    countries = ['Корея Южная', 'Аргентина', 'Испания', 'Франция', 'Нидерланды', 'Швейцария', 'Португалия', 'Беларусь',
                 'Германия', 'Италия', 'Канада', 'Япония', 'Бразилия', 'Новая Зеландия', 'Австрия', 'Колумбия', 'Китай',
                 'Дания', 'Мексика', 'ОАЭ', 'США', 'Швеция', 'Казахстан', 'ЮАР', 'Великобритания', 'Россия']
    country_buttons = [InlineKeyboardButton(text=country, callback_data=f"country:{country}") for country in countries]
    country_markup = InlineKeyboardMarkup(row_width=3)
    country_markup.add(*country_buttons)
    return country_markup


def pagination_create_genre_selection_keyboard_full_setup():
    # Создаем клавиатуру для выбора жанра
    genres = ["комедия", "драма", "боевик", "фантастика", "ужасы", "приключения", "триллер", "фэнтези", "детектив",
              "криминал", "вестерн", "военный", "мелодрама", "мультфильм", "короткометражка", "детский", "биография",
              "история", "аниме", "семейный"]
    genre_buttons = [InlineKeyboardButton(text=genre, callback_data=f"genre:{genre}") for genre in genres]
    genres_markup = InlineKeyboardMarkup(row_width=3)
    genres_markup.add(*genre_buttons)
    return genres_markup


def pagination_create_year_selection_keyboard_full_setup():
    """Создайте клавиатуру с опциями выбора года"""
    year_ranges = ["1990-2000", "2001-2005", "2006-2010", "2011-2015", "2016-2020", "2021-2024"]

    year_buttons = [InlineKeyboardButton(text=year_range, callback_data=f"year:{year_range}") for year_range in
                    year_ranges]
    year_markup = InlineKeyboardMarkup(row_width=3)
    year_markup.add(*year_buttons)
    return year_markup


def pagination_top_create_rating_random_movie_by_rating_keyboard_full_setup():
    """Создайте клавиатуру с возможностью выбора рейтинга"""
    top_ratings = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10']

    top_rating_buttons = [InlineKeyboardButton(text=top_rating, callback_data=f"top_rating:{top_rating}") for top_rating
                          in top_ratings]
    top_rating_markup = InlineKeyboardMarkup(row_width=3)
    top_rating_markup.add(*top_rating_buttons)
    return top_rating_markup


class PaginationGenreSelectionState(StatesGroup):
    pagination_genre_selection = State()
    pagination_country_selection = State()
    pagination_year_selection = State()
    pagination_top_rating_selection = State()


@dp.message_handler(lambda message: message.text == "🎲 5 случайных фильмов полный выбор")
async def pagination_top_random_movie_command_full_setup(message: types.Message):
    chat_id = message.chat.id
    main_page_kb = five_films_complete_selection_keyboard()
    await bot.send_message(chat_id, "🎲 5 случайных фильмов полный выбор", reply_markup=main_page_kb)
    genres_markup_user = pagination_create_genre_selection_keyboard_full_setup()
    await message.answer("Выберите жанр фильма:", reply_markup=genres_markup_user)
    await PaginationGenreSelectionState.pagination_genre_selection.set()


@dp.callback_query_handler(pagination_genre_callback_full_setup.filter(),
                           state=PaginationGenreSelectionState.pagination_genre_selection)
async def pagination_full_user_selection_genre(query: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(genre=callback_data["genre"])
    country_markup = pagination_create_genre_random_movie_full_setup_keyboard()
    await bot.send_message(query.message.chat.id, "Выберите страну происхождения фильма:", reply_markup=country_markup)
    await PaginationGenreSelectionState.pagination_country_selection.set()


@dp.callback_query_handler(pagination_full_user_selection_country_callback.filter(),
                           state=PaginationGenreSelectionState.pagination_country_selection)
async def pagination_full_user_selection_country(query: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(country=callback_data["country"])
    year_markup = pagination_create_year_selection_keyboard_full_setup()
    await bot.send_message(query.message.chat.id, "Выберите диапазон лет:", reply_markup=year_markup)
    await PaginationGenreSelectionState.pagination_year_selection.set()


@dp.callback_query_handler(pagination_year_callback_full_setup.filter(),
                           state=PaginationGenreSelectionState.pagination_year_selection)
async def pagination_full_user_selection_year(query: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.update_data(year=callback_data["year"])
    top_rating_markup = pagination_top_create_rating_random_movie_by_rating_keyboard_full_setup()
    await bot.send_message(query.message.chat.id, "Выберите рейтинг фильма:", reply_markup=top_rating_markup)
    await PaginationGenreSelectionState.pagination_top_rating_selection.set()


@dp.callback_query_handler(pagination_top_rating_callback_full_setup.filter(),
                           state=PaginationGenreSelectionState.pagination_top_rating_selection)
async def pagination_full_user_selection_top_rating(query: CallbackQuery, state: FSMContext, callback_data: dict):
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
        for i in range(5):
            movie_info, poster_url = get_random_movie_by_genre_year_rating_country(
                f"{genre},{year_range},{country},{top_rating}")
            items_random_full_setup[i] = [movie_info, poster_url]
        try:
            await bot.send_photo(chat_id, photo=items_random_full_setup[0][1], caption=items_random_full_setup[0][0],
                                 reply_markup=pagination_random_full_setup(0))
        except aiogram.utils.exceptions.BadRequest:
            await bot.send_message(chat_id, "Фильмы по выбранным параметрам не найдены.")
    except TypeError:
        await bot.send_message(chat_id, "Фильмы по выбранным параметрам не найдены.")

    await state.finish()


pag_cb_random_full_setup = CallbackData("empty", "action", "page")
items_random_full_setup = {}


def pagination_random_full_setup(page: int = 0, total_pages: int = 5):
    buttons = [InlineKeyboardButton("⬅", callback_data=pag_cb_random_full_setup.new(action="prev", page=page)),
               InlineKeyboardButton("➡", callback_data=pag_cb_random_full_setup.new(action="next", page=page))]
    if page == 0:  # Remove the "prev" button if at the beginning
        buttons.pop(0)
    if page == total_pages - 1:  # Remove the "next" button if at the end
        buttons.pop()
    return InlineKeyboardMarkup().row(*buttons)


@dp.callback_query_handler(pag_cb_random_full_setup.filter(action="prev"))
async def prev_page(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) - 1 if int(callback_data["page"]) > 0 else 0
    await query.message.edit_media(InputMediaPhoto(media=items_random_full_setup[page][1]))
    await query.message.edit_caption(caption=items_random_full_setup[page][0],
                                     reply_markup=pagination_random_full_setup(page))


@dp.callback_query_handler(pag_cb_random_full_setup.filter(action="next"))
async def next_page(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) + 1
    try:
        await query.message.edit_media(InputMediaPhoto(media=items_random_full_setup[page][1]))
        await query.message.edit_caption(caption=items_random_full_setup[page][0],
                                         reply_markup=pagination_random_full_setup(page))
    except KeyError as error:
        logger.exception(error)


def register_random_5_movie_command_handler_full_setup():
    dp.register_message_handler(pagination_top_random_movie_command_full_setup)
    dp.register_callback_query_handler(pagination_full_user_selection_genre,
                                       pagination_genre_callback_full_setup.filter())
    dp.register_callback_query_handler(pagination_full_user_selection_country,
                                       pagination_full_user_selection_country_callback.filter())
    dp.register_callback_query_handler(pagination_full_user_selection_year,
                                       pagination_year_callback_full_setup.filter())
    dp.register_callback_query_handler(pagination_full_user_selection_top_rating,
                                       pagination_top_rating_callback_full_setup.filter())
