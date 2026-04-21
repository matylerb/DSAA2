class Movie:

    def __init__(self, movie_id, title, genres):
        self.movie_id = int(movie_id)
        self.title = title
        self.genres = genres

    def __repr__(self):
        return f"Movie(id={self.movie_id}, title='{self.title}', genres='{self.genres}')"

    def __str__(self):
        return f"[{self.movie_id}] {self.title} | {self.genres}"
