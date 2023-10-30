import aiogram.utils.exceptions
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.callback_data import CallbackData

from database.database import get_random_movie_by_country
from keyboards.reply.categories_btn import create_pagination_country_keyboard
from system.dispatcher import dp, bot

user_selections_country = {}  # Create a dictionary to store user selections
pag_cb_country = CallbackData("empty", "action", "page")
top_country_callback = CallbackData("top_country_random", "top_country_random")
country_items = {}


def create_genre_random_movie_by_top_country_keyboard():
    """Создайте клавиатуру с возможностью выбора жанра"""
    top_countries = ['Корея Южная', 'Аргентина', 'Испания', 'Франция', 'Нидерланды', 'Швейцария', 'Португалия',
                     'Беларусь', 'Германия', 'Италия', 'Канада', 'Япония', 'Бразилия', 'Новая Зеландия', 'Австрия',
                     'Колумбия', 'Китай', 'Дания', 'Мексика', 'ОАЭ', 'США', 'Швеция', 'Казахстан', 'ЮАР',
                     'Великобритания', 'Россия']

    top_country_buttons = [InlineKeyboardButton(text=top_country, callback_data=f"top_country_random:{top_country}") for
                           top_country in
                           top_countries]
    country_markup = InlineKeyboardMarkup(row_width=3)
    country_markup.add(*top_country_buttons)
    return country_markup


@dp.message_handler(lambda message: message.text == "🎲 5 случайных фильмов по стране")
async def random_movie_command_country(message: types.Message):
    chat_id = message.chat.id
    main_page_kb = create_pagination_country_keyboard()
    await bot.send_message(chat_id, "🎲 5 случайных фильмов по стране происхождения", reply_markup=main_page_kb)
    country_markup = create_genre_random_movie_by_top_country_keyboard()  # Клавиатура выбора жанра фильма
    await message.answer("Выберите страну происхождения фильма:", reply_markup=country_markup)


@dp.callback_query_handler(top_country_callback.filter())
async def country_process_year_callback_1(query: CallbackQuery):
    chat_id = query.message.chat.id
    top_country = query.data.split(":")[1]
    user_selections_country[chat_id] = {"top_country_random": top_country}
    print(top_country)

    user_choice_message = (f"🎬 5 случайных фильмов\n\n"
                           f"🎭 Страна: <b>{top_country}</b>,\n\n"
                           f"<code>Если фильмы по выбранной стране не найдены, то будут добавлены позже. "
                           f"Мы постоянно расширяемся и создаем свою базу, не зависимую от внешних источников.</code>")

    await bot.send_message(chat_id, user_choice_message)
    await bot.send_chat_action(chat_id, 'typing')  # Показываем индикатор "бот печатает"
    for i in range(5):
        movie_info, poster_url = get_random_movie_by_country(top_country)
        country_items[i] = [movie_info, poster_url]
    try:
        await bot.send_photo(chat_id, photo=country_items[0][1], caption=country_items[0][0],
                             reply_markup=top_paginator_country(0))
    except aiogram.utils.exceptions.BadRequest:
        await bot.send_message(chat_id, "Извините, возникла проблема с отправкой фильмов. Попробуйте еще раз. По вашему запросу фильмы не найдены")


def top_paginator_country(page: int = 0, total_pages: int = 5):
    buttons = [InlineKeyboardButton("⬅", callback_data=pag_cb_country.new(action="prev_country", page=page)),
               InlineKeyboardButton("➡", callback_data=pag_cb_country.new(action="next_country", page=page))]
    if page == 0:  # Remove the "prev" button if at the beginning
        buttons.pop(0)
    if page == total_pages - 1:  # Remove the "next" button if at the end
        buttons.pop()
    return InlineKeyboardMarkup().row(*buttons)


@dp.callback_query_handler(pag_cb_country.filter(action="prev_country"))
async def prev_page(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) - 1 if int(callback_data["page"]) > 0 else 0
    await query.message.edit_media(InputMediaPhoto(media=country_items[page][1]))
    await query.message.edit_caption(caption=country_items[page][0], reply_markup=top_paginator_country(page))


@dp.callback_query_handler(pag_cb_country.filter(action="next_country"))
async def next_page(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data["page"]) + 1
    await query.message.edit_media(InputMediaPhoto(media=country_items[page][1]))
    await query.message.edit_caption(caption=country_items[page][0], reply_markup=top_paginator_country(page))


def register_random_movie_country():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(random_movie_command_country)  # Обработчик команды /random
