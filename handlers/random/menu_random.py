from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.reply.categories_btn import create_menu_random_keyboard
from system.dispatcher import dp, bot


@dp.message_handler(lambda message: message.text == "🍿 Случайный фильм")
async def menu_random(message: types.Message, state: FSMContext):
    """Главная страница бота"""
    await state.finish()
    await state.reset_state()
    with open("media/photos/greeting.jpg", "rb") as photo_file:  # Загружаем фото для поста
        categories_kb = create_menu_random_keyboard()
        post_greeting = ('Меню выбора случайных фильмов, вы можете рандомно получить:\n\n'
                         '🎬 Случайный фильм,\n'
                         '🎬 Случайный фильм по жанру,\n'
                         '🎬 Случайный фильм по стране,\n'
                         '🎬 Случайный фильм по рейтингу,\n'
                         '🎬 Cлучайный фильм полный выбор\n\n')
        await bot.send_photo(message.from_user.id, caption=post_greeting, photo=photo_file, reply_markup=categories_kb)


def register_menu_random_handler():
    """Меню выбора случайных фильмов"""
    dp.register_message_handler(menu_random)
