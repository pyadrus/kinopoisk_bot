from aiogram import types
from aiogram.dispatcher import FSMContext

from database.database import count_rows_in_database, read_channels_from_database, DATABASE_FILE
from handlers.admin_handlers import is_user_subscribed
from keyboards.reply.categories_btn import create_categories_keyboard
from system.dispatcher import dp, bot


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия 👋"""
    user_id = message.from_user.id
    channel_usernames = read_channels_from_database(DATABASE_FILE)  # Получаем список групп/каналов из базы данных

    if await is_user_subscribed(user_id):
        await state.finish()  # Завершаем текущее состояние машины состояний
        await state.reset_state()  # Сбрасываем все данные машины состояний, до значения по умолчанию
        with open("media/photos/greeting.jpg", "rb") as photo_file:  # Загружаем фото для поста
            categories_kb = create_categories_keyboard()
            count = count_rows_in_database()
            post_greeting = ('Привет! 👋🎥 Я твой личный кинобот.\n\n'
                             'Я помогу тебе найти лучшие фильмы, расскажу об актерах, подскажу рейтинги и многое другое.\n\n'
                             'Просто спрашивай, и я помогу найти идеальный фильм для твоего настроения! 😊🍿🎬'
                             f'Бот имеет обширную базу в {count} фильмов 🎥')
            await bot.send_photo(message.from_user.id, caption=post_greeting, photo=photo_file,
                                 reply_markup=categories_kb)
    else:
        await bot.send_message(message.from_user.id, f"<blockquote>‼️Для того чтобы пользоваться ботом 🔗@CineSearch24_bot, вы должны быть участником следующих групп/каналов:\n\n"
                            f"{' '.join(channel_usernames)}\n\n"
                            f"Если вы уже подписаны или подписались, нажмите: ➡️ /start.</blockquote>\n\n"
                            f"Если по какой-то причине бот все равно не отвечает, напишите разработчику @PyAdminRU")


@dp.message_handler(lambda message: message.text == "⬅️ На главную")
async def greeting_home(message: types.Message, state: FSMContext):
    """Главная страница бота"""
    await state.finish()
    await state.reset_state()
    with open("media/photos/greeting.jpg", "rb") as photo_file:  # Загружаем фото для поста
        categories_kb = create_categories_keyboard()
        count = count_rows_in_database()
        post_greeting = ('Привет! 👋🎥 Я твой личный кинобот.\n\n'
                         'Я помогу тебе найти лучшие фильмы, расскажу об актерах, подскажу рейтинги и многое другое.\n\n'
                         f'Просто спрашивай, и я помогу найти идеальный фильм для твоего настроения! 😊🍿🎬\n\n'
                         f'Бот имеет обширную базу в {count} фильмов 🎥')
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
