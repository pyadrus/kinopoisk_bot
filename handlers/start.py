from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.reply.categories_btn import create_categories_keyboard
from system.dispatcher import dp, bot


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия 👋"""
    await state.finish()  # Завершаем текущее состояние машины состояний
    await state.reset_state()  # Сбрасываем все данные машины состояний, до значения по умолчанию
    with open("media/photos/greeting.jpg", "rb") as photo_file:  # Загружаем фото для поста
        categories_kb = create_categories_keyboard()
        post_greeting = ('Привет! 👋🎥 Я твой личный кинобот.\n\n'
                         'Я помогу тебе найти лучшие фильмы, расскажу об актерах, подскажу рейтинги и многое другое.\n\n'
                         'Просто спрашивай, и я помогу найти идеальный фильм для твоего настроения! 😊🍿🎬')
        await bot.send_photo(message.from_user.id, caption=post_greeting, photo=photo_file, reply_markup=categories_kb)


@dp.callback_query_handler(lambda c: c.data == "disagree")
async def disagree_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Вот список команд доступных на данный момент:\n'
                                        '/help - информация о командах\n'
                                        '/search - простой поиск фильма по названию\n'
                                        '/adv_search - поиск фильма по фильтрам\n'
                                        '/random - получить случайный фильм из базы\n')


def register_greeting_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(greeting)  # Обработчик команды /start, он же пост приветствия 👋
    dp.register_message_handler(disagree_handler)
