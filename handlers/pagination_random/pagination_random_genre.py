import aiogram.utils.exceptions
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.callback_data import CallbackData

from database.database import get_random_movie_by_genre_and_year
from keyboards.inline.adv_search_again import create_genre_selection_keyboard, create_year_selection_keyboard
from keyboards.reply.categories_btn import create_pagination_random_genre_keyboard
from system.dispatcher import dp, bot

user_selections = {}  # Create a dictionary to store user selections
pag_cb_1 = CallbackData("empty", "action", "page")
year_callback = CallbackData("year", "year")
items_1 = {}
genre_callback = CallbackData("genre", "genre")


@dp.message_handler(lambda message: message.text == "🎲 5 случайных фильмов по жанрам")
async def random_movie_command_genres_1(message: types.Message):
    chat_id = message.chat.id
    main_page_kb = create_pagination_random_genre_keyboard()
    await bot.send_message(chat_id, "🎲 5 случайных фильмов по жанрам", reply_markup=main_page_kb)
    genres_markup = create_genre_selection_keyboard()  # Клавиатура выбора жанра фильма
    await message.answer("Выберите жанр фильма:", reply_markup=genres_markup)


@dp.callback_query_handler(genre_callback.filter())
async def process_genre_callback_genres(query: CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    genre = callback_data["genre"]
    user_selections[chat_id] = {"genre": genre}
    year_markup = create_year_selection_keyboard()  # Клавиатура выбора диапазона лет
    await bot.send_message(chat_id, "Выберите диапазон лет:", reply_markup=year_markup)


@dp.callback_query_handler(year_callback.filter())
async def process_year_callback_1(query: CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    year_range = callback_data["year"]
    genre = user_selections.get(chat_id, {}).get("genre", "Unknown")

    user_choice_message = (f"🎬 5 случайных фильмов\n\n"
                           f"🎭 Жанр: <b>{genre}</b>,\n"
                           f"📅 Год выпуска: <b>{year_range}</b>. 🎥\n\n"
                           f"<code>Если фильмы по выбранному году и жанру не найдены, то будут добавлены позже. "
                           f"Мы постоянно расширяемся и создаем свою базу, не зависимую от внешних источников.</code>")

    await bot.send_message(chat_id, user_choice_message)
    await bot.send_chat_action(chat_id, 'typing')  # Показываем индикатор "бот печатает"
    for i in range(5):
        movie_info, poster_url = get_random_movie_by_genre_and_year(f"{genre},{year_range}")
        items_1[i] = [movie_info, poster_url]
    try:
        await bot.send_photo(chat_id, photo=items_1[0][1], caption=items_1[0][0], reply_markup=paginator_1(0))
    except aiogram.utils.exceptions.BadRequest:
        await bot.send_message(chat_id, "Извините, возникла проблема с отправкой фильмов. Попробуйте еще раз. По вашему запросу фильмы не найдены")


def paginator_1(page: int = 0, total_pages: int = 5):
    buttons = [InlineKeyboardButton("⬅", callback_data=pag_cb_1.new(action="prev", page=page)),
               InlineKeyboardButton("➡", callback_data=pag_cb_1.new(action="next", page=page))]
    if page == 0:  # Remove the "prev" button if at the beginning
        buttons.pop(0)
    if page == total_pages - 1:  # Remove the "next" button if at the end
        buttons.pop()
    return InlineKeyboardMarkup().row(*buttons)


@dp.callback_query_handler(pag_cb_1.filter(action="prev"))
async def prev_page(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) - 1 if int(callback_data["page"]) > 0 else 0
    await query.message.edit_media(InputMediaPhoto(media=items_1[page][1]))
    await query.message.edit_caption(caption=items_1[page][0], reply_markup=paginator_1(page))


@dp.callback_query_handler(pag_cb_1.filter(action="next"))
async def next_page(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) + 1
    await query.message.edit_media(InputMediaPhoto(media=items_1[page][1]))
    await query.message.edit_caption(caption=items_1[page][0], reply_markup=paginator_1(page))


def register_random_10_movie_command_handler_genres_1():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(random_movie_command_genres_1)  # Обработчик команды /random
