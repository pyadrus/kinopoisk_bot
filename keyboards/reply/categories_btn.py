from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_categories_keyboard():
	# one_time_keyboard=False - клавиатура не скрывается
	categories_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	random_btn = KeyboardButton('Случайный фильм')
	search_btn = KeyboardButton('Случайные фильм по жанрам')
	random_btn_10 = KeyboardButton('10 cлучайных фильмов')
	search_btn_genre = KeyboardButton("5 случайных фильмов по жанрам")
	categories_kb.add(random_btn, search_btn)
	categories_kb.add(random_btn_10, search_btn_genre)
	return categories_kb


if __name__ == '__main__':
	create_categories_keyboard()
