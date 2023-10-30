import aiogram.utils.exceptions
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.callback_data import CallbackData

from database.database import get_random_id_movies, get_movie_info
from keyboards.reply.categories_btn import create_pagination_top_handlers_keyboard
from system.dispatcher import dp, bot

items = {}


@dp.message_handler(lambda message: message.text == "🎲 5 случайных фильмов")
async def random_movie_command(message: types.Message):
    chat_id = message.chat.id
    main_page_kb = create_pagination_top_handlers_keyboard()
    await bot.send_message(chat_id, "🎲 5 случайных фильмов", reply_markup=main_page_kb)
    await bot.send_chat_action(chat_id, 'typing')  # Показываем индикатор "бот печатает"
    for i in range(5):
        random_id_movies = get_random_id_movies()
        movie_info, poster_url = get_movie_info(random_id_movies)
        items[i] = [movie_info, poster_url]
    try:
        # Use message.answer_photo with the URL directly
        await bot.send_photo(chat_id, photo=items[0][1], caption=items[0][0], reply_markup=paginator(0))
    except aiogram.utils.exceptions.BadRequest:
        # Handle the exception by informing the user that there was an issue
        await bot.send_message(chat_id,
                               "Извините, возникла проблема с отправкой фильмов. Попробуйте еще раз. По вашему запросу фильмы не найдены")


pag_cb = CallbackData("empty", "action", "page")


def paginator(page_1: int = 0, total_pages_1: int = 5):
    buttons = [InlineKeyboardButton("⬅", callback_data=pag_cb.new(action="prev_1", page=page_1)),
               InlineKeyboardButton("➡", callback_data=pag_cb.new(action="next_1", page=page_1))]
    # Remove the "prev" button if at the beginning
    if page_1 == 0:
        buttons.pop(0)
    # Remove the "next" button if at the end
    if page_1 == total_pages_1 - 1:
        buttons.pop()

    return InlineKeyboardMarkup().row(*buttons)


@dp.callback_query_handler(pag_cb.filter(action="prev_1"))
async def prev_page_1(query: types.CallbackQuery, callback_data: dict):
    page_1 = int(callback_data["page"]) - 1 if int(callback_data["page"]) > 0 else 0
    try:
        await query.message.edit_media(InputMediaPhoto(media=items[page_1][1]))
        await query.message.edit_caption(caption=items[page_1][0], reply_markup=paginator(page_1))
    except IndexError:
        # Handle the case where the page is out of bounds
        await query.answer("No more previous pages available.")


@dp.callback_query_handler(pag_cb.filter(action="next_1"))
async def next_page_1(query: types.CallbackQuery, callback_data: dict):
    chat_id = query.message.chat.id
    page_1 = int(callback_data["page"]) + 1
    try:
        await query.message.edit_media(InputMediaPhoto(media=items[page_1][1]))
        await query.message.edit_caption(caption=items[page_1][0], reply_markup=paginator(page_1))
    except IndexError:
        # Handle the case where the page is out of bounds
        await query.answer("No more next pages available.")
    except aiogram.utils.exceptions.BadRequest:
        await bot.send_message(chat_id, "Извините, возникла проблема с отправкой фильмов. Попробуйте еще раз")


def register_random_10_movie_command_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(random_movie_command)  # Обработчик команды /random
