import csv
from model.movies import Movie


class DataLoader:

    def __init__(self, file_path):
        self.file_path = file_path
        self.__movies = []
        self._load_movies()

    def _load_movies(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                movie = Movie(
                    movie_id=row['movieId'],
                    title=row['title'],
                    genres=row['genres'],
                )
                self.__movies.append(movie)

    def get_all_data(self):
        return self.__movies.copy()

    def get_data_by_size(self, size):
        if size > len(self.__movies):
            raise ValueError(
                f"Requested size {size} exceeds available {len(self.__movies)} records."
            )
        return self.__movies[:size].copy()
