from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_categories_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    categories_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    random_btn = KeyboardButton('🎬 Случайный фильм')
    search_btn = KeyboardButton('🎬 Случайный фильм по жанру')
    search_btn_country = KeyboardButton('🎬 Случайный фильм по стране')
    search_btn_ratings = KeyboardButton('🎬 Случайный фильм по рейтингу')
    random_btn_10 = KeyboardButton('🎲 5 случайных фильмов')
    search_btn_genre = KeyboardButton("🎲 5 случайных фильмов по жанрам")
    home_page_btn = KeyboardButton("⬅️ На главную")
    categories_kb.add(random_btn, search_btn)
    categories_kb.add(search_btn_country, search_btn_ratings)
    categories_kb.add(random_btn_10, search_btn_genre)
    categories_kb.add(home_page_btn)
    return categories_kb


def create_random_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    main_page_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    random_btn = KeyboardButton('🎬 Случайный фильм')
    # search_btn = KeyboardButton('🎬 Случайный фильм по жанру')
    # search_btn_country = KeyboardButton('🎬 Случайный фильм по стране')
    # search_btn_ratings = KeyboardButton('🎬 Случайный фильм по рейтингу')
    # random_btn_10 = KeyboardButton('🎲 5 случайных фильмов')
    # search_btn_genre = KeyboardButton("🎲 5 случайных фильмов по жанрам")
    home_page_btn = KeyboardButton("⬅️ На главную")
    # categories_kb.add(random_btn, search_btn)
    # categories_kb.add(search_btn_country, search_btn_ratings)
    # categories_kb.add(random_btn_10, search_btn_genre)
    main_page_kb.add(home_page_btn, random_btn)
    return main_page_kb


if __name__ == '__main__':
    create_categories_keyboard()
