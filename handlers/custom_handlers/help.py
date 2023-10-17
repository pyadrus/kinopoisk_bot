from aiogram import types
from system.dispatcher import dp


@dp.message_handler(commands=['help'])
async def hello_replier(message: types.Message):
    """
	Хендлер для обработки команды /help
	"""
    await message.answer('Вот список команд доступных на данный момент:\n'
                         '/help - информация о командах\n'
                         '/search - простой поиск фильма по названию\n'
                         '/adv_search - поиск фильма по фильтрам\n'
                         '/random - получить случайный фильм из базы'
                         '/genre - рандомный фильм по жанрам\n')


def register_hello_replier_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(hello_replier)  # Обработчик команды /help, он же пост приветствия 👋
