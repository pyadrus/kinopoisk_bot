import aiogram.utils.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.callback_data import CallbackData
from loguru import logger

from database.database import get_random_movie_by_genre_and_year
from keyboards.inline.adv_search_again import create_genre_selection_keyboard
from keyboards.reply.categories_btn import create_pagination_random_genre_keyboard
from system.dispatcher import dp, bot

logger.add("logs/log.log", retention="1 days", enqueue=True)  # Логирование бота

year_callback = CallbackData("year", "year")
genre_callback = CallbackData("genre", "genre")


class PaginationRandomGenre(StatesGroup):  # Класс для хранения состояний машины состояний
    paginator_random_genre_state = State()  # Жанр
    paginator_year_state = State()  # Год


@dp.message_handler(lambda message: message.text == "🎲 5 случайных фильмов по жанрам")
async def random_movie_command_genres_1(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    # await state.finish()  # Завершаем текущее состояние машины состояний
    # await state.reset_state()  # Сбрасываем все данные машины состояний, до значения по умолчанию
    main_page_kb = create_pagination_random_genre_keyboard()
    await bot.send_message(chat_id, "🎲 5 случайных фильмов по жанрам", reply_markup=main_page_kb)
    genres_markup = create_genre_selection_keyboard()  # Клавиатура выбора жанра фильма
    await message.answer("Выберите жанр фильма:", reply_markup=genres_markup)
    await PaginationRandomGenre.paginator_random_genre_state.set()


def create_year_selection_genre_keyboard():
    """Создайте клавиатуру с опциями выбора года"""
    year_ranges = ["1990-2000", "2001-2005", "2006-2010", "2011-2015", "2016-2020", "2021-2024"]
    year_buttons = [InlineKeyboardButton(text=year_range, callback_data=f"year:{year_range}") for year_range in
                    year_ranges]
    year_markup = InlineKeyboardMarkup(row_width=3)
    year_markup.add(*year_buttons)
    return year_markup


@dp.callback_query_handler(genre_callback.filter(), state=PaginationRandomGenre.paginator_random_genre_state)
async def process_genre_callback_genres(query: CallbackQuery, state: FSMContext, callback_data: dict):
    chat_id = query.message.chat.id
    genre = callback_data["genre"]
    logger.info(f"Выбранный жанр: {genre}, пользователь: {chat_id}")
    await state.update_data(genre=callback_data["genre"])
    year_markup = create_year_selection_genre_keyboard()  # Клавиатура выбора диапазона лет
    await bot.send_message(chat_id, "Выберите диапазон лет:", reply_markup=year_markup)
    await PaginationRandomGenre.paginator_year_state.set()


@dp.callback_query_handler(year_callback.filter(), state=PaginationRandomGenre.paginator_year_state)
async def process_year_callback_1(query: CallbackQuery, state: FSMContext, callback_data: dict):
    chat_id = query.message.chat.id
    data = await state.get_data()
    genre = data.get("genre", "")
    year_range = callback_data["year"]
    logger.info(f"Выбранный год: {year_range}, пользователь: {chat_id}")

    user_choice_message = (f"🎬 5 случайных фильмов\n\n"
                           f"🎭 Жанр: <b>{genre}</b>,\n"
                           f"📅 Год выпуска: <b>{year_range}</b>. 🎥\n\n"
                           f"<code>Если фильмы по выбранному году и жанру не найдены, то будут добавлены позже. "
                           f"Мы постоянно расширяемся и создаем свою базу, не зависимую от внешних источников.</code>")

    await bot.send_message(chat_id, user_choice_message)
    await bot.send_chat_action(chat_id, 'typing')  # Показываем индикатор "бот печатает"
    for i in range(5):
        movie_info, poster_url = get_random_movie_by_genre_and_year(f"{genre},{year_range}")
        items_paginator_random_genre[i] = [movie_info, poster_url]
    logger.info(f"Выбранные фильмы: {items_paginator_random_genre}")
    try:
        await bot.send_photo(chat_id, photo=items_paginator_random_genre[0][1], caption=items_paginator_random_genre[0][0],
                             reply_markup=paginator_random_genre(0))
    except aiogram.utils.exceptions.BadRequest:
        await bot.send_message(chat_id,
                               "Извините, возникла проблема с отправкой фильмов. Попробуйте еще раз. По вашему запросу фильмы не найдены")
    await state.finish()

items_paginator_random_genre = {}
pag_cb_1 = CallbackData("empty", "action", "page")


def paginator_random_genre(page: int = 0, total_pages: int = 5):
    buttons = [InlineKeyboardButton("⬅", callback_data=pag_cb_1.new(action="prevs", page=page)),
               InlineKeyboardButton("➡", callback_data=pag_cb_1.new(action="nexts", page=page))]
    if page == 0:  # Remove the "prev" button if at the beginning
        buttons.pop(0)
    if page == total_pages - 1:  # Remove the "next" button if at the end
        buttons.pop()
    return InlineKeyboardMarkup().row(*buttons)


@dp.callback_query_handler(pag_cb_1.filter(action="prevs"))
async def prev_page_pagination_random_genre(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) - 1 if int(callback_data["page"]) > 0 else 0
    logger.info(f"Следующий фильм из 5 рандомных фильмов по жанру: {page}")
    await query.message.edit_media(InputMediaPhoto(media=items_paginator_random_genre[page][1]))
    await query.message.edit_caption(caption=items_paginator_random_genre[page][0], reply_markup=paginator_random_genre(page))


@dp.callback_query_handler(pag_cb_1.filter(action="nexts"))
async def next_page_pagination_random_genre(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) + 1
    if 0 <= page < len(items_paginator_random_genre):
        try:
            await query.message.edit_media(InputMediaPhoto(media=items_paginator_random_genre[page][1]))
            await query.message.edit_caption(caption=items_paginator_random_genre[page][0], reply_markup=paginator_random_genre(page))
        except Exception as error:
            logger.exception(error)
    else:
        # Handle the case where the page is out of bounds (e.g., reached the end of the list).
        # You can send a message indicating that there are no more movies.
        await query.message.answer("No more movies available.")


def register_random_10_movie_command_handler_genres_1():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(random_movie_command_genres_1)  # Обработчик команды /random
    dp.register_callback_query_handler(process_year_callback_1, year_callback.filter())
    dp.register_callback_query_handler(process_genre_callback_genres, genre_callback.filter())
