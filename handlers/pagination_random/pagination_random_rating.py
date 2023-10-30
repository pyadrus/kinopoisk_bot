import aiogram.utils.exceptions
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.callback_data import CallbackData

from database.database import get_random_movie_by_country, get_random_movie_by_ratings
from keyboards.reply.categories_btn import create_pagination_country_keyboard, create_pagination_rating_keyboard
from system.dispatcher import dp, bot

user_selections_rating = {}  # Create a dictionary to store user selections
pag_cb_rating = CallbackData("empty", "action", "page")
top_rating_callback = CallbackData("top_rating_random", "top_rating_random")
rating_items = {}


def top_create_rating_random_movie_by_rating_keyboard():
    """Создайте клавиатуру с возможностью выбора рейтинга"""
    top_ratings = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10']

    top_rating_buttons = [InlineKeyboardButton(text=top_rating, callback_data=f"top_rating_random:{top_rating}") for top_rating in top_ratings]
    top_rating_markup = InlineKeyboardMarkup(row_width=3)
    top_rating_markup.add(*top_rating_buttons)
    return top_rating_markup


@dp.message_handler(lambda message: message.text == "🎲 5 случайных фильмов по рейтингу")
async def random_movie_command_rating(message: types.Message):
    chat_id = message.chat.id
    main_page_kb = create_pagination_rating_keyboard()
    await bot.send_message(chat_id, "🎲 5 случайных фильмов по рейтингу", reply_markup=main_page_kb)
    top_rating_markup = top_create_rating_random_movie_by_rating_keyboard()  # Клавиатура выбора жанра фильма
    await message.answer("Выберите страну происхождения фильма:", reply_markup=top_rating_markup)


@dp.callback_query_handler(top_rating_callback.filter())
async def rating_process_year_callback_1(query: CallbackQuery):
    chat_id = query.message.chat.id
    top_rating = query.data.split(":")[1]
    user_selections_rating[chat_id] = {"top_country_random": top_rating}
    print(top_rating)

    user_choice_message = (f"🎬 5 случайных фильмов\n\n"
                           f"🎭 Рейтинг: <b>{top_rating}</b>,\n\n"
                           f"<code>Если фильмы по выбранной стране не найдены, то будут добавлены позже. "
                           f"Мы постоянно расширяемся и создаем свою базу, не зависимую от внешних источников.</code>")

    await bot.send_message(chat_id, user_choice_message)
    await bot.send_chat_action(chat_id, 'typing')  # Показываем индикатор "бот печатает"
    for i in range(5):
        movie_info, poster_url = get_random_movie_by_ratings(top_rating)
        rating_items[i] = [movie_info, poster_url]
    try:
        await bot.send_photo(chat_id, photo=rating_items[0][1], caption=rating_items[0][0],
                             reply_markup=top_paginator_country(0))
    except aiogram.utils.exceptions.BadRequest:
        await bot.send_message(chat_id, "Извините, возникла проблема с отправкой фильмов. Попробуйте еще раз. По вашему запросу фильмы не найдены")


def top_paginator_country(page: int = 0, total_pages: int = 5):
    buttons = [InlineKeyboardButton("⬅", callback_data=pag_cb_rating.new(action="prev_rating", page=page)),
               InlineKeyboardButton("➡", callback_data=pag_cb_rating.new(action="next_rating", page=page))]
    if page == 0:  # Remove the "prev" button if at the beginning
        buttons.pop(0)
    if page == total_pages - 1:  # Remove the "next" button if at the end
        buttons.pop()
    return InlineKeyboardMarkup().row(*buttons)


@dp.callback_query_handler(pag_cb_rating.filter(action="prev_rating"))
async def prev_page(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) - 1 if int(callback_data["page"]) > 0 else 0
    await query.message.edit_media(InputMediaPhoto(media=rating_items[page][1]))
    await query.message.edit_caption(caption=rating_items[page][0], reply_markup=top_paginator_country(page))


@dp.callback_query_handler(pag_cb_rating.filter(action="next_rating"))
async def next_page(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) + 1
    await query.message.edit_media(InputMediaPhoto(media=rating_items[page][1]))
    await query.message.edit_caption(caption=rating_items[page][0], reply_markup=top_paginator_country(page))


def register_random_movie_rating():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(random_movie_command_rating)  # Обработчик команды /random
