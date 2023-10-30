from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from database.database import get_random_movie_by_ratings
from keyboards.reply.categories_btn import create_random_rating_keyboard
from system.dispatcher import dp, bot


def create_rating_random_movie_by_rating_keyboard():
    """Создайте клавиатуру с возможностью выбора рейтинга"""
    ratings = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10']

    rating_buttons = [InlineKeyboardButton(text=rating, callback_data=f"rating_random:{rating}") for rating in ratings]
    rating_markup = InlineKeyboardMarkup(row_width=3)
    rating_markup.add(*rating_buttons)
    return rating_markup


@dp.message_handler(lambda message: message.text == "🎬 Случайный фильм по рейтингу")
async def random_movie_by_rating(message: types.Message):
    chat_id = message.chat.id
    main_page_kb = create_random_rating_keyboard()
    await bot.send_message(chat_id, "🎬 Случайный фильм по рейтингу", reply_markup=main_page_kb)
    rating_markup = create_rating_random_movie_by_rating_keyboard()  # Клавиатура выбора жанра фильма
    await message.answer("Выберите рейтинг для фильма:", reply_markup=rating_markup)


random_movie_by_rating_callback = CallbackData("rating_random", "rating_random")
random_movie_by_rating_user_selections = {}  # Create a dictionary to store user selections


@dp.callback_query_handler(random_movie_by_rating_callback.filter())
async def process_random_movie_by_rating(query: CallbackQuery):
    chat_id = query.message.chat.id
    rating = query.data.split(":")[1]
    random_movie_by_rating_user_selections[chat_id] = {"rating_random": rating}
    print(rating)
    await bot.send_chat_action(chat_id, 'typing')  # Show the "bot is typing" indicator
    try:
        movie_info, poster_url = get_random_movie_by_ratings(rating)
        await bot.send_photo(chat_id, photo=poster_url, caption=movie_info)
    except TypeError:
        await bot.send_message(chat_id, "Извините, возникла проблема с отправкой фильмов. Попробуйте еще раз. По вашему запросу фильмы не найдены")

def register_random_rating_handler():
    dp.register_message_handler(random_movie_by_rating)
