from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.reply.categories_btn import five_create_categories_keyboard
from system.dispatcher import dp, bot


@dp.message_handler(lambda message: message.text == "🍿 5 случайных фильмов")
async def pagination_menu_random(message: types.Message, state: FSMContext):
    """Главная страница бота"""
    await state.finish()
    await state.reset_state()
    with open("media/photos/greeting.jpg", "rb") as photo_file:  # Загружаем фото для поста
        categories_kb = five_create_categories_keyboard()
        post_greeting = ('Меню выбора случайных фильмов, вы можете рандомно получить:\n\n'
                         '🎲 5 случайных фильмов\n'
                         '🎲 5 случайных фильмов по жанрам,\n'
                         '🎲 5 случайных фильмов по стране,\n'
                         '🎲 5 случайных фильмов по рейтингу,\n'
                         '🎲 5 случайных фильмов полный выбор.\n')
        await bot.send_photo(message.from_user.id, caption=post_greeting, photo=photo_file, reply_markup=categories_kb)


def pagination_register_menu_random_handler():
    """Меню выбора случайных фильмов"""
    dp.register_message_handler(pagination_menu_random)
