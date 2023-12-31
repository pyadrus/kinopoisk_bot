from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_categories_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    categories_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    random_btn = KeyboardButton('🍿 Случайный фильм')
    random_btn_10 = KeyboardButton('🍿 5 случайных фильмов')
    categories_kb.add(random_btn, random_btn_10)
    return categories_kb


def five_create_categories_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    categories_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    random_btn_10 = KeyboardButton('🎲 5 случайных фильмов')
    search_btn_genre = KeyboardButton("🎲 5 случайных фильмов по жанрам")
    top_search_btn_country = KeyboardButton('🎲 5 случайных фильмов по стране')
    top_search_btn_ratings = KeyboardButton('🎲 5 случайных фильмов по рейтингу')
    top_search_btn_full_setup = KeyboardButton('🎲 5 случайных фильмов полный выбор')
    home_page_btn = KeyboardButton("⬅️ На главную")
    categories_kb.add(random_btn_10, search_btn_genre)
    categories_kb.add(top_search_btn_country, top_search_btn_ratings)
    categories_kb.add(top_search_btn_full_setup)
    categories_kb.add(home_page_btn)
    return categories_kb


def create_menu_random_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    categories_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    random_btn = KeyboardButton('🎬 Случайный фильм')
    search_btn = KeyboardButton('🎬 Случайный фильм по жанру')
    search_btn_country = KeyboardButton('🎬 Случайный фильм по стране')
    search_btn_ratings = KeyboardButton('🎬 Случайный фильм по рейтингу')
    search_btn_full_setup = KeyboardButton('🎬 Случайный фильм полный выбор')
    home_page_btn = KeyboardButton("⬅️ На главную")
    categories_kb.add(random_btn, search_btn)
    categories_kb.add(search_btn_country, search_btn_ratings)
    categories_kb.add(search_btn_full_setup)
    categories_kb.add(home_page_btn)
    return categories_kb


def create_random_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    main_page_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    random_btn = KeyboardButton('🎬 Случайный фильм')
    home_page_btn = KeyboardButton("⬅️ На главную")
    main_page_kb.add(home_page_btn, random_btn)
    return main_page_kb


def create_pagination_random_genre_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    main_page_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    search_btn_genre = KeyboardButton("🎲 5 случайных фильмов по жанрам")
    home_page_btn = KeyboardButton("⬅️ На главную")
    main_page_kb.add(home_page_btn, search_btn_genre)
    return main_page_kb


def create_random_genre_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    main_page_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    search_btn = KeyboardButton('🎬 Случайный фильм по жанру')
    home_page_btn = KeyboardButton("⬅️ На главную")
    main_page_kb.add(home_page_btn, search_btn)
    return main_page_kb


def create_random_rating_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    main_page_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    search_btn_ratings = KeyboardButton('🎬 Случайный фильм по рейтингу')
    home_page_btn = KeyboardButton("⬅️ На главную")
    main_page_kb.add(home_page_btn, search_btn_ratings)
    return main_page_kb


def create_random_country_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    main_page_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    search_btn_country = KeyboardButton('🎬 Случайный фильм по стране')
    home_page_btn = KeyboardButton("⬅️ На главную")
    main_page_kb.add(home_page_btn, search_btn_country)
    return main_page_kb


def create_pagination_top_handlers_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    main_page_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    random_btn_10 = KeyboardButton('🎲 5 случайных фильмов')
    home_page_btn = KeyboardButton("⬅️ На главную")
    main_page_kb.add(home_page_btn, random_btn_10)
    return main_page_kb


def create_pagination_country_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    main_page_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    random_btn_10 = KeyboardButton('🎲 5 случайных фильмов по стране')
    home_page_btn = KeyboardButton("⬅️ На главную")
    main_page_kb.add(home_page_btn, random_btn_10)
    return main_page_kb


def create_pagination_rating_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    main_page_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    random_btn_10 = KeyboardButton('🎲 5 случайных фильмов по рейтингу')
    home_page_btn = KeyboardButton("⬅️ На главную")
    main_page_kb.add(home_page_btn, random_btn_10)
    return main_page_kb


def five_films_complete_selection_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    main_page_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    random_btn_10 = KeyboardButton('🎲 5 случайных фильмов полный выбор')
    home_page_btn = KeyboardButton("⬅️ На главную")
    main_page_kb.add(home_page_btn, random_btn_10)
    return main_page_kb


def films_complete_selection_keyboard():
    # one_time_keyboard=False - клавиатура не скрывается
    main_page_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    random_btn_10 = KeyboardButton('🎬 Случайный фильм полный выбор')
    home_page_btn = KeyboardButton("⬅️ На главную")
    main_page_kb.add(home_page_btn, random_btn_10)
    return main_page_kb


if __name__ == '__main__':
    create_categories_keyboard()
    five_create_categories_keyboard()
    create_menu_random_keyboard()
    create_random_keyboard()
    create_pagination_random_genre_keyboard()
    create_random_genre_keyboard()
    create_random_rating_keyboard()
    create_random_country_keyboard()
    create_pagination_top_handlers_keyboard()
    create_pagination_country_keyboard()
    create_pagination_rating_keyboard()
    five_films_complete_selection_keyboard()
    films_complete_selection_keyboard()