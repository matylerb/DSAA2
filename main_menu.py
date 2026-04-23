from data_loader.data_loader import DataLoader
from business.movie_collection import MovieCollection
from sorter.hash import HashMap
from sorter.trie import Trie
import time


def print_menu():
    print("====================================")
    print("Movie Search — Hash Map & Trie Demo")
    print("====================================")
    print("1. Show total movies loaded")
    print("2. Exact search by title (Hash Map)")
    print("3. Exact search by Movie ID (Hash Map)")
    print("4. Prefix search (Trie autocomplete)")
    print("5. Rebuild structures with different dataset size")
    print("6. Exit")
    print("====================================\n")


def build_structures(collection):
    hash_map = HashMap()
    trie = Trie()

    start = time.perf_counter()
    collection.build_hash_map(hash_map)
    hm_time = time.perf_counter() - start

    start = time.perf_counter()
    collection.build_trie(trie)
    trie_time = time.perf_counter() - start

    print(f"  HashMap built in {hm_time:.6f}s (load factor: {hash_map.load_factor():.4f})")
    print(f"  Trie built in    {trie_time:.6f}s\n")
    return hash_map, trie


def main():
    loader = DataLoader("data/movies.csv")
    size = 1000
    movies = loader.get_data_by_size(size)
    collection = MovieCollection("MovieLens", movies)

    print(f"\nLoaded {size} movies. Building data structures...\n")
    hash_map, trie = build_structures(collection)

    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()

        match choice:
            case '1':
                print(f"\nTotal movies: {collection.total_movies()}\n")

            case '2':
                query = input("Enter exact movie title: ").strip()
                start = time.perf_counter()
                result = collection.search_exact(hash_map, query)
                elapsed = time.perf_counter() - start
                if result:
                    print(f"\nFound: {result}  [{elapsed:.8f}s]\n")
                else:
                    print(f"\nNo movie found for '{query}'  [{elapsed:.8f}s]\n")

            case '3':
                try:
                    movie_id = int(input("Enter Movie ID: ").strip())
                except ValueError:
                    print("Invalid ID.\n")
                    continue
                start = time.perf_counter()
                result = collection.search_by_id(hash_map, movie_id)
                elapsed = time.perf_counter() - start
                if result:
                    print(f"\nFound: {result}  [{elapsed:.8f}s]\n")
                else:
                    print(f"\nNo movie found with ID {movie_id}  [{elapsed:.8f}s]\n")

            case '4':
                prefix = input("Enter title prefix: ").strip()
                start = time.perf_counter()
                matches = collection.search_prefix(trie, prefix)
                elapsed = time.perf_counter() - start
                print(f"\n{len(matches)} match(es) for '{prefix}'  [{elapsed:.8f}s]:")
                for movie in matches[:10]:
                    print(f"  {movie}")
                if len(matches) > 10:
                    print(f"  ... and {len(matches) - 10} more")
                print()

            case '5':
                try:
                    size = int(input("Enter dataset size: ").strip())
                    movies = loader.get_data_by_size(size)
                    collection.set_movies(movies)
                    print(f"\nRebuilding with {size} movies...\n")
                    hash_map, trie = build_structures(collection)
                except ValueError as e:
                    print(f"Error: {e}\n")

            case '6':
                print("Goodbye!")
                break

            case _:
                print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
