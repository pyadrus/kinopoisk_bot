import aiogram.utils.exceptions
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

from database.database import get_random_movie_by_genre_keyword
from database.movie_api_requests import get_random_movie_genres
from keyboards.inline.adv_search_again import create_genre_selection_keyboard, create_year_selection_keyboard, \
    year_callback
from system.dispatcher import dp, bot

items_1 = {}


@dp.message_handler(lambda message: message.text == "5 случайных фильмов по жанрам")
async def random_movie_command_genres_1(message: types.Message):
    chat_id = message.chat.id
    await bot.send_chat_action(chat_id, 'typing')  # Показываем индикатор "бот печатает"
    genres_markup = create_genre_selection_keyboard()
    print(genres_markup)
    await message.answer("Выберите жанр фильма:", reply_markup=genres_markup)


genre_callback = CallbackData("genre", "genre")
user_selections = {}  # Create a dictionary to store user selections


@dp.callback_query_handler(genre_callback.filter())
async def process_genre_callback_genres_1(query: CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    genre = callback_data["genre"]
    user_selections[chat_id] = {"genre": genre}
    global global_genre  # Access the global variable
    global_genre = genre
    await choose_year_genres_1(query)


async def choose_year_genres_1(query: CallbackQuery):
    chat_id = query.message.chat.id
    year_markup = create_year_selection_keyboard()
    await bot.send_message(chat_id, "Выберите диапазон лет:", reply_markup=year_markup)


@dp.callback_query_handler(year_callback.filter())
async def process_year_callback_1(query: CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    year_range = callback_data["year"]
    genre = user_selections.get(chat_id, {}).get("genre", "Unknown")
    await bot.send_message(chat_id, "Вот 10 случайных фильмов, по жанру:")
    await bot.send_chat_action(chat_id, 'typing')  # Показываем индикатор "бот печатает"
    for i in range(5):
        movie_info, poster_url = get_random_movie_genres(genre, year_range)
        print(movie_info)
        items_1[i] = [movie_info, poster_url]
    print(items_1)
    try:
        # Use message.answer_photo with the URL directly
        await bot.answer_photo(photo=items_1[0][1], caption=items_1[0][0], reply_markup=paginator_1(0))
    except aiogram.utils.exceptions.BadRequest:
        print("Ошибка BadRequest")
        # movie_info, poster_url = get_random_movie_by_genre_keyword(genre)
        await bot.send_message(chat_id, text=items_1[0][0], reply_markup=paginator_1(0))
    except aiogram.utils.exceptions.MessageTextIsEmpty:
        movie_info, poster_url = get_random_movie_by_genre_keyword(global_genre)
        items_1[0] = [movie_info, poster_url]
        await query.message.edit_media(InputMediaPhoto(media=items_1[0][1]))
        await query.message.edit_caption(caption=items_1[0][0], reply_markup=paginator_1(0))


pag_cb_1 = CallbackData("empty", "action", "page")


def paginator_1(page: int = 0, total_pages: int = 5):
    buttons = [InlineKeyboardButton("⬅", callback_data=pag_cb_1.new(action="prev", page=page)),
               InlineKeyboardButton("➡", callback_data=pag_cb_1.new(action="next", page=page))]
    if page == 0:  # Remove the "prev" button if at the beginning
        buttons.pop(0)
    if page == total_pages - 1:  # Remove the "next" button if at the end
        buttons.pop()
    return InlineKeyboardMarkup().row(*buttons)

global_genre = ""

@dp.callback_query_handler(pag_cb_1.filter(action="prev"))
async def prev_page_genres_1(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) - 1 if int(callback_data["page"]) > 0 else 0
    await query.message.edit_media(InputMediaPhoto(media=items_1[page][1]))
    await query.message.edit_caption(caption=items_1[page][0], reply_markup=paginator_1(page))


@dp.callback_query_handler(pag_cb_1.filter(action="next"))
async def next_page_genres_1(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) + 1
    global global_genre  # Access the global genre
    try:
        await query.message.edit_media(InputMediaPhoto(media=items_1[page][1]))
        await query.message.edit_caption(caption=items_1[page][0], reply_markup=paginator_1(page))

    except aiogram.utils.exceptions.BadRequest:
        movie_info, poster_url = get_random_movie_by_genre_keyword(global_genre)
        items_1[page] = [movie_info, poster_url]
        try:
            await query.message.edit_media(InputMediaPhoto(media=items_1[page][1]))
            await query.message.edit_caption(caption=items_1[0][0], reply_markup=paginator_1(page))
        except aiogram.utils.exceptions.BadRequest:
            movie_info, poster_url = get_random_movie_by_genre_keyword(global_genre)
            items_1[page] = [movie_info, poster_url]
            await query.message.edit_media(InputMediaPhoto(media=items_1[page][1]))
            await query.message.edit_caption(caption=items_1[0][0], reply_markup=paginator_1(page))


@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler_1(update, error):
    return True


def register_random_10_movie_command_handler_genres_1():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(random_movie_command_genres_1)  # Обработчик команды /random
