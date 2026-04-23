import csv
import os
import time

from data_loader.data_loader import DataLoader
from business.movie_collection import MovieCollection
from sorter.hash import HashMap
from sorter.trie import Trie


def write_results_to_csv(results, filepath, headers, row_fn):
    """Write a list of result rows to a CSV file."""
    dirname = os.path.dirname(filepath)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for item in results:
            writer.writerow(row_fn(item))


def demo_exact_search(collection, size):
    """Insert movies into a HashMap and perform exact searches."""
    print("====================================")
    print(f"HashMap — Exact Search (n={size})")
    print("====================================\n")

    hash_map = HashMap()

    start = time.perf_counter()
    collection.build_hash_map(hash_map)
    build_time = time.perf_counter() - start
    print(f"  Build time : {build_time:.6f} seconds")
    print(f"  Load factor: {hash_map.load_factor():.4f}\n")

    queries = ["toy story (1995)", "jumanji (1995)", "heat (1995)", "unknown title xyz"]
    print("  Exact title searches:")
    for q in queries:
        start = time.perf_counter()
        result = collection.search_exact(hash_map, q)
        elapsed = time.perf_counter() - start
        status = str(result) if result else "Not found"
        print(f"    '{q}' -> {status}  [{elapsed:.8f}s]")

    print()
    return hash_map, build_time


def demo_prefix_search(collection, size):
    """Insert movies into a Trie and perform prefix searches."""
    print("====================================")
    print(f"Trie — Prefix Search (n={size})")
    print("====================================\n")

    trie = Trie()

    start = time.perf_counter()
    collection.build_trie(trie)
    build_time = time.perf_counter() - start
    print(f"  Build time: {build_time:.6f} seconds\n")

    prefixes = ["toy", "the", "star", "inc"]
    print("  Prefix searches:")
    for prefix in prefixes:
        start = time.perf_counter()
        matches = collection.search_prefix(trie, prefix)
        elapsed = time.perf_counter() - start
        print(f"    '{prefix}' -> {len(matches)} match(es)  [{elapsed:.8f}s]")
        for movie in matches[:3]:
            print(f"      {movie}")
        if len(matches) > 3:
            print(f"      ... and {len(matches) - 3} more")
        print()

    return trie, build_time


if __name__ == "__main__":
    print("====================================")
    print("Movie Search Demo — Hash Map & Trie")
    print("====================================\n")

    loader = DataLoader("data/movies.csv")
    size = 1000
    movies = loader.get_data_by_size(size)

    collection = MovieCollection("MovieLens", movies)
    print(f"Loaded {collection.total_movies()} movies\n")

    hash_map, hm_build = demo_exact_search(collection, size)
    trie, trie_build = demo_prefix_search(collection, size)

    # Write prefix search sample output
    sample_prefix = "the"
    matches = collection.search_prefix(trie, sample_prefix)
    write_results_to_csv(
        matches,
        "output/prefix_search_the.csv",
        ["movie_id", "title", "genres"],
        lambda m: [m.movie_id, m.title, m.genres],
    )
    print(f"Prefix search results for '{sample_prefix}' written to output/prefix_search_the.csv")
