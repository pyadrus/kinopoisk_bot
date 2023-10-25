from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

year_callback = CallbackData("year", "year")


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
    year_ranges = ["1990-1995", "1996-2000", "2001-2005", "2006-2010", "2011-2015", "2016-2020", "2021-2023"]
    year_markup = InlineKeyboardMarkup(row_width=3)
    year_buttons = [InlineKeyboardButton(text=year_range, callback_data=year_callback.new(year=year_range)) for
                    year_range in year_ranges]
    year_markup.add(*year_buttons)
    return year_markup


if __name__ == '__main__':
    create_genre_selection_keyboard()
    create_year_selection_keyboard()
