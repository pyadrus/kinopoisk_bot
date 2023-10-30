from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_categories_keyboard():
	# one_time_keyboard=False - клавиатура не скрывается
	categories_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
	random_btn = KeyboardButton('🎬 Случайный фильм')
	search_btn = KeyboardButton('🎬 Случайный фильм по жанру')
	random_btn_10 = KeyboardButton('🎲 5 случайных фильмов')
	search_btn_genre = KeyboardButton("🎲 5 случайных фильмов по жанрам")
	home_page_btn = KeyboardButton("⬅️ На главную")
	categories_kb.add(random_btn, search_btn)
	categories_kb.add(random_btn_10, search_btn_genre)
	categories_kb.add(home_page_btn)
	return categories_kb


if __name__ == '__main__':
	create_categories_keyboard()
