import time

from data_loader.data_loader import DataLoader
from sorter.hash import HashMap
from sorter.trie import Trie


RUNS = 3
SIZES = [500, 1000, 2000, 4000, 8000]
PREFIXES = ["the", "star", "inc", "to"]


def time_insert_hashmap(movies, runs=RUNS):
    total = 0
    for _ in range(runs):
        hm = HashMap()
        start = time.perf_counter()
        for movie in movies:
            hm.insert(movie.title.lower(), movie)
            hm.insert(str(movie.movie_id), movie)
        total += time.perf_counter() - start
    return total / runs


def time_insert_trie(movies, runs=RUNS):
    total = 0
    for _ in range(runs):
        t = Trie()
        start = time.perf_counter()
        for movie in movies:
            t.insert(movie.title.lower(), movie)
        total += time.perf_counter() - start
    return total / runs


def time_exact_search_hashmap(movies, runs=RUNS):
    hm = HashMap()
    for movie in movies:
        hm.insert(movie.title.lower(), movie)
    queries = [m.title.lower() for m in movies[:10]]
    total = 0
    for _ in range(runs):
        start = time.perf_counter()
        for q in queries:
            hm.search(q)
        total += time.perf_counter() - start
    return (total / runs) / len(queries)


def time_exact_search_linear(movies, runs=RUNS):
    queries = [m.title.lower() for m in movies[:10]]
    total = 0
    for _ in range(runs):
        start = time.perf_counter()
        for q in queries:
            for m in movies:
                if m.title.lower() == q:
                    break
        total += time.perf_counter() - start
    return (total / runs) / len(queries)


def time_prefix_search_trie(movies, prefix, runs=RUNS):
    t = Trie()
    for movie in movies:
        t.insert(movie.title.lower(), movie)
    total = 0
    for _ in range(runs):
        start = time.perf_counter()
        t.prefix_search(prefix)
        total += time.perf_counter() - start
    return total / runs


def time_prefix_search_linear(movies, prefix, runs=RUNS):
    total = 0
    for _ in range(runs):
        start = time.perf_counter()
        _ = [m for m in movies if m.title.lower().startswith(prefix)]
        total += time.perf_counter() - start
    return total / runs


def main():
    loader = DataLoader("data/movies.csv")

    # ------------------------------------------------------------------
    # Insertion benchmarks
    # ------------------------------------------------------------------
    print("=== Insertion Time (avg of 3 runs, seconds) ===")
    header = f"{'Size':<8}{'HashMap':<18}{'Trie':<18}"
    print(header)
    print("-" * len(header))
    for size in SIZES:
        movies = loader.get_data_by_size(size)
        hm_t = time_insert_hashmap(movies)
        tr_t = time_insert_trie(movies)
        print(f"{size:<8}{hm_t:<18.6f}{tr_t:<18.6f}")

    print()

    # ------------------------------------------------------------------
    # Exact search benchmarks
    # ------------------------------------------------------------------
    print("=== Exact Search Time per Query (avg of 3 runs, seconds) ===")
    header = f"{'Size':<8}{'HashMap':<18}{'Linear Scan':<18}"
    print(header)
    print("-" * len(header))
    for size in SIZES:
        movies = loader.get_data_by_size(size)
        hm_t = time_exact_search_hashmap(movies)
        ln_t = time_exact_search_linear(movies)
        print(f"{size:<8}{hm_t:<18.8f}{ln_t:<18.8f}")

    print()

    # ------------------------------------------------------------------
    # Prefix search benchmarks
    # ------------------------------------------------------------------
    for prefix in PREFIXES:
        print(f"=== Prefix Search '{prefix}' (avg of 3 runs, seconds) ===")
        header = f"{'Size':<8}{'Trie':<18}{'Linear Scan':<18}"
        print(header)
        print("-" * len(header))
        for size in SIZES:
            movies = loader.get_data_by_size(size)
            tr_t = time_prefix_search_trie(movies, prefix)
            ln_t = time_prefix_search_linear(movies, prefix)
            print(f"{size:<8}{tr_t:<18.8f}{ln_t:<18.8f}")
        print()


if __name__ == "__main__":
    main()
