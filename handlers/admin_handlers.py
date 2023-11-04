import logging
import sqlite3  # Добавьте импорт библиотеки SQLite3

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.filters.state import StatesGroup

from database.database import read_channels_from_database, DATABASE_FILE
from system.dispatcher import dp, bot


# Команда для добавления канала в базу данных
class SomeState(StatesGroup):
    AddingChannel = State()
    RemovingChannel = State()


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    """Команда для проверки подписки"""
    help_text = ("Добро пожаловать!😊\n"
                 "Команды:\n\n"
                 "/help — справка📝\n"
                 "/add_group_id — добавить канал в базу данных🔬\n"
                 "/remove_group_id — удалить канал из базы данных🔨\n")
    await message.reply(help_text)


async def is_user_subscribed(user_id):
    """Функция для проверки подписки пользователя на несколько каналов"""
    CHANNEL_USERNAMES = read_channels_from_database(DATABASE_FILE)
    try:
        for channel_username in CHANNEL_USERNAMES:
            user = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
            if user.status not in ('member', 'administrator', 'creator'):
                return False
        return True
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        return False


@dp.message_handler(commands=['add_group_id'])
async def cmd_add_group_id(message: types.Message):
    user_id = message.from_user.id
    if message.chat.type == types.ChatType.PRIVATE:
        await message.reply("Введите username канала, который вы хотите добавить в базу данных:")
        await SomeState.AddingChannel.set()
    else:
        await message.reply("Эта команда доступна только в личных сообщениях (DM).")


@dp.message_handler(state=SomeState.AddingChannel)
async def process_channel_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['channel_username'] = message.text
        try:
            # Попробуйте подключиться к базе данных и добавить username канала
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS channels (channel_username)")
            cursor.execute("INSERT INTO channels (channel_username) VALUES (?)", (data['channel_username'],))
            conn.commit()
            conn.close()
            await message.reply(f"Канал {data['channel_username']} добавлен в базу данных.")
        except Exception as e:
            logging.error(f"Error adding channel to database: {e}")
            await message.reply("Произошла ошибка при добавлении канала в базу данных. Попробуйте позже.")
        await state.finish()


async def remove_channel_from_database(channel_username):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM channels WHERE channel_username = ?", (channel_username,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logging.error(f"Error removing channel from database: {e}")
        return False


@dp.message_handler(commands=['remove_group_id'])
async def cmd_remove_group_id(message: types.Message):
    user_id = message.from_user.id
    if message.chat.type == types.ChatType.PRIVATE:
        await message.reply("Введите username канала, который вы хотите удалить из базы данных:")
        await SomeState.RemovingChannel.set()
    else:
        await message.reply("Эта команда доступна только в личных сообщениях (DM).")


@dp.message_handler(state=SomeState.RemovingChannel)
async def process_remove_channel_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        channel_username = message.text
        if await remove_channel_from_database(channel_username):
            await message.reply(f"Канал {channel_username} удален из базы данных.")
        else:
            await message.reply("Произошла ошибка при удалении канала из базы данных. Попробуйте позже.")
        await state.finish()


def register_admin_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(cmd_help)
    dp.register_message_handler(cmd_add_group_id)
    dp.register_message_handler(cmd_remove_group_id)