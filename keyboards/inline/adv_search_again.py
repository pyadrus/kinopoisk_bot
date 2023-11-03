from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_genre_selection_keyboard():
    """Создайте клавиатуру с возможностью выбора жанра"""
    genres = ["комедия", "драма", "боевик", "фантастика", "ужасы", "приключения", "триллер", "фэнтези", "детектив",
              "криминал", "вестерн", "военный", "мелодрама", "мультфильм", "короткометражка", "детский", "биография",
              "история", "аниме", "семейный"]
    genre_buttons = [InlineKeyboardButton(text=genre, callback_data=f"genre:{genre}") for genre in genres]
    genres_markup = InlineKeyboardMarkup(row_width=3)
    genres_markup.add(*genre_buttons)
    return genres_markup



def create_year_selection_keyboard():
    """Создайте клавиатуру с опциями выбора года"""
    year_ranges = ["1990-2000", "2001-2005", "2006-2010", "2011-2015", "2016-2020", "2021-2024"]

    year_buttons = [InlineKeyboardButton(text=year_range, callback_data=f"year:{year_range}") for year_range in
                    year_ranges]
    year_markup = InlineKeyboardMarkup(row_width=3)
    year_markup.add(*year_buttons)
    return year_markup


def create_rating_random_movie_full_setup():
    """Создайте клавиатуру с возможностью выбора рейтинга"""
    ratings = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10']

    rating_buttons = [InlineKeyboardButton(text=rating, callback_data=f"rating_random:{rating}") for rating in ratings]
    rating_markup = InlineKeyboardMarkup(row_width=3)
    rating_markup.add(*rating_buttons)
    return rating_markup


def create_genre_random_movie_full_setup_keyboard():
    """Создайте клавиатуру с возможностью выбора жанра"""
    countries = ['Корея Южная', 'Аргентина', 'Испания', 'Франция', 'Нидерланды', 'Швейцария', 'Португалия', 'Беларусь',
                 'Германия', 'Италия', 'Канада', 'Япония', 'Бразилия', 'Новая Зеландия', 'Австрия', 'Колумбия', 'Китай',
                 'Дания', 'Мексика', 'ОАЭ', 'США', 'Швеция', 'Казахстан', 'ЮАР', 'Великобритания', 'Россия']

    country_buttons = [InlineKeyboardButton(text=country, callback_data=f"country_random:{country}") for country in
                       countries]
    country_markup = InlineKeyboardMarkup(row_width=3)
    country_markup.add(*country_buttons)
    return country_markup


if __name__ == '__main__':
    create_genre_selection_keyboard()
    create_year_selection_keyboard()
    create_rating_random_movie_full_setup()
    create_genre_random_movie_full_setup_keyboard()
