from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.reply.categories_btn import create_categories_keyboard
from system.dispatcher import dp


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия 👋"""
    await state.finish()  # Завершаем текущее состояние машины состояний
    await state.reset_state()  # Сбрасываем все данные машины состояний, до значения по умолчанию
    categories_kb = create_categories_keyboard()
    await message.answer('Вот список команд доступных на данный момент:\n'
                         '/help - информация о командах\n'
                         '/search - простой поиск фильма по названию\n'
                         '/adv_search - поиск фильма по фильтрам\n'
                         '/random - получить случайный фильм из базы\n', reply_markup=categories_kb)


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
