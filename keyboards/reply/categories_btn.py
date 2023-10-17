from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_categories_keyboard():
	categories_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	random_btn = KeyboardButton('Случайный фильм')
	search_btn = KeyboardButton('Случайные фильм по жанрам')
	categories_kb.add(random_btn, search_btn)
	return categories_kb


if __name__ == '__main__':
	create_categories_keyboard()
