from aiogram import types
from aiogram.dispatcher import FSMContext
from system.dispatcher import dp


@dp.message_handler(commands=['start'])
async def greeting(message: types.Message, state: FSMContext):
    """Обработчик команды /start, он же пост приветствия 👋"""
    await state.finish()  # Завершаем текущее состояние машины состояний
    await state.reset_state()  # Сбрасываем все данные машины состояний, до значения по умолчанию

    await message.answer('Вот список команд доступных на данный момент:\n'
                         '/help - информация о командах\n'
                         '/search - простой поиск фильма по названию\n'
                         '/adv_search - поиск фильма по фильтрам\n'
                         '/random - получить случайный фильм из базы\n')


@dp.callback_query_handler(lambda c: c.data == "disagree")
async def disagree_handler(callback_query: types.CallbackQuery, state: FSMContext):
    from_user_name = callback_query.from_user.first_name  # Получаем фамилию пользователя
    await callback_query.message.answer('Вот список команд доступных на данный момент:\n'
                                        '/help - информация о командах\n'
                                        '/search - простой поиск фильма по названию\n'
                                        '/adv_search - поиск фильма по фильтрам\n'
                                        '/random - получить случайный фильм из базы\n')


def greeting_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(greeting)  # Обработчик команды /start, он же пост приветствия 👋
    dp.register_message_handler(disagree_handler)
