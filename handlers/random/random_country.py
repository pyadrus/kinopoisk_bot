from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from database.database import get_random_movie_by_country
from keyboards.reply.categories_btn import create_random_country_keyboard
from system.dispatcher import dp, bot


def create_genre_random_movie_by_country_keyboard():
    """Создайте клавиатуру с возможностью выбора жанра"""
    countries = ['Корея Южная', 'Аргентина', 'Испания', 'Франция', 'Нидерланды', 'Швейцария', 'Португалия', 'Беларусь',
                 'Германия', 'Италия', 'Канада', 'Япония', 'Бразилия', 'Новая Зеландия', 'Австрия', 'Колумбия', 'Китай',
                 'Дания', 'Мексика', 'ОАЭ', 'США', 'Швеция', 'Казахстан', 'ЮАР', 'Великобритания', 'Россия']

    country_buttons = [InlineKeyboardButton(text=country, callback_data=f"country_random:{country}") for country in
                       countries]
    country_markup = InlineKeyboardMarkup(row_width=3)
    country_markup.add(*country_buttons)
    return country_markup


@dp.message_handler(lambda message: message.text == "🎬 Случайный фильм по стране")
async def random_movie_by_country(message: types.Message):
    chat_id = message.chat.id
    main_page_kb = create_random_country_keyboard()
    await bot.send_message(chat_id, "🎬 Случайный фильм по стране", reply_markup=main_page_kb)
    country_markup = create_genre_random_movie_by_country_keyboard()  # Клавиатура выбора жанра фильма
    await message.answer("Выберите страну происхождения фильма:", reply_markup=country_markup)


random_movie_by_country_callback = CallbackData("country_random", "country_random")
random_movie_by_country_user_selections = {}  # Create a dictionary to store user selections


@dp.callback_query_handler(random_movie_by_country_callback.filter())
async def process_random_movie_by_country(query: CallbackQuery):
    chat_id = query.message.chat.id
    country = query.data.split(":")[1]
    random_movie_by_country_user_selections[chat_id] = {"country_random": country}
    print(country)
    await bot.send_chat_action(chat_id, 'typing')  # Show the "bot is typing" indicator
    movie_info, poster_url = get_random_movie_by_country(country)
    await bot.send_photo(chat_id, photo=poster_url, caption=movie_info)


def register_random_country_handler():
    dp.register_message_handler(random_movie_by_country)
