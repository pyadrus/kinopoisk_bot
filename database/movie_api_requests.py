import random

import requests

from database.database import recording_movies_in_the_database
from system.dispatcher import API_KEY


def get_random_movie_genres(genres, year_range):
    headers = {'X-API-KEY': API_KEY}
    response = requests.get('https://api.kinopoisk.dev/v1.3/movie',
                            params={"genres.name": genres, "limit": 1, "page": 1, "year": year_range},
                            headers=headers)
    if response.status_code == 200:
        movies = response.json()
        print(movies)
        total_pages = movies["total"] // movies["limit"] + (1 if movies["total"] % movies["limit"] > 0 else 0)
        random_page = random.randint(1, total_pages)
        response = requests.get('https://api.kinopoisk.dev/v1.3/movie',
                                params={"genres.name": genres, "limit": 1, "page": random_page, "year": year_range},
                                headers=headers)
        if response.status_code == 200:
            movie = response.json()['docs'][0]  # Get the first movie from the response
            print(movie)
            id_movies = movie.get('id')
            print(id_movies)
            name = movie.get('names', [{}])[0].get('name', 'Название фильма не найдено')
            year = movie.get('year', 'Год выпуска не найден')
            rating = movie['rating'].get('kp', 'Рейтинг не найден')
            description = movie.get('description', 'Описание отсутствует')  # Handle missing 'description' key
            genres = ', '.join([genre.get('name', '') for genre in movie.get('genres', [])])
            countries = ', '.join([country.get('name', '') for country in movie.get('countries', [])])
            poster = movie.get('poster')
            poster_url = poster.get('url', 'https://yt3.googleusercontent.com/b2Rf6ON5kiJEiq8EvYWYuQcX8M_c2nODMPcJMKW4-iY8iOY2AHDHS6JT47bKSY9AlVg3tOOWJPE=s900-c-k-c0x00ffffff-no-rj')  # Provide your default poster URL
            movie_info = (f'Название: {name}\n'
                          f'Год выпуска: {year}\n'
                          f'Рейтинг Кинопоиска: {rating}\n'
                          f'Жанры: {genres}\n'
                          f'Страна: {countries}\n\n'
                          f'Описание: {description}\n')
            recording_movies_in_the_database(id_movies, name, year, rating, description, genres, countries, poster_url)
            return movie_info, poster_url
        else:
            return None, None
    else:
        return None, None