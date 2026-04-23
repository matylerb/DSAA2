class MovieCollection:

    def __init__(self, name, movies=None):
        self.name = name
        self.__movies = movies if movies else []

    def add_movie(self, movie):
        self.__movies.append(movie)

    def get_movies(self):
        return self.__movies.copy()

    def set_movies(self, movies):
        self.__movies = movies if movies else []

    def total_movies(self):
        return len(self.__movies)

    def build_hash_map(self, hash_map):
        """Insert all movies into a HashMap keyed by lowercase title and by movie_id."""
        for movie in self.__movies:
            hash_map.insert(movie.title.lower(), movie)
            hash_map.insert(str(movie.movie_id), movie)

    def build_trie(self, trie):
        """Insert all movie titles into a Trie."""
        for movie in self.__movies:
            trie.insert(movie.title.lower(), movie)

    def search_exact(self, hash_map, key):
        """Exact lookup via HashMap."""
        return hash_map.search(key.lower())

    def search_by_id(self, hash_map, movie_id):
        """Exact lookup by movie ID via HashMap."""
        return hash_map.search(str(movie_id))

    def search_prefix(self, trie, prefix):
        """Prefix-based search via Trie."""
        return trie.prefix_search(prefix.lower())
