import random
import time
import matplotlib.pyplot as plt

from data_loader.data_loader import DataLoader
from sorter.hash import HashMap
from sorter.trie import Trie


SIZES = [500, 1000, 2000, 4000, 8000, 16000, 32000]
RUNS = 5
PREFIX = "the"


def time_build(structure_cls, movies, runs=RUNS):
    total = 0
    for _ in range(runs):
        s = structure_cls()
        start = time.perf_counter()
        for movie in movies:
            if structure_cls is HashMap:
                s.insert(movie.title.lower(), movie)
                s.insert(str(movie.movie_id), movie)
            else:
                s.insert(movie.title.lower(), movie)
        total += time.perf_counter() - start
    return total / runs


def time_exact_hashmap(movies, runs=RUNS):
    hm = HashMap()
    for movie in movies:
        hm.insert(movie.title.lower(), movie)
    queries = [m.title.lower() for m in random.sample(movies, min(20, len(movies)))]
    total = 0
    for _ in range(runs):
        start = time.perf_counter()
        for q in queries:
            hm.search(q)
        total += time.perf_counter() - start
    return (total / runs) / len(queries)


def time_exact_linear(movies, runs=RUNS):
    queries = [m.title.lower() for m in random.sample(movies, min(20, len(movies)))]
    total = 0
    for _ in range(runs):
        start = time.perf_counter()
        for q in queries:
            for m in movies:
                if m.title.lower() == q:
                    break
        total += time.perf_counter() - start
    return (total / runs) / len(queries)


def time_prefix_trie(movies, prefix, runs=RUNS):
    t = Trie()
    for movie in movies:
        t.insert(movie.title.lower(), movie)
    total = 0
    for _ in range(runs):
        start = time.perf_counter()
        t.prefix_search(prefix)
        total += time.perf_counter() - start
    return total / runs


def time_prefix_linear(movies, prefix, runs=RUNS):
    total = 0
    for _ in range(runs):
        start = time.perf_counter()
        _ = [m for m in movies if m.title.lower().startswith(prefix)]
        total += time.perf_counter() - start
    return total / runs


def main():
    loader = DataLoader("data/movies.csv")

    hm_build_times = []
    trie_build_times = []
    hm_exact_times = []
    linear_exact_times = []
    trie_prefix_times = []
    linear_prefix_times = []

    print("Running benchmarks...\n")

    for size in SIZES:
        print(f"  n={size}", end="", flush=True)
        movies = loader.get_data_by_size(size)

        hm_build_times.append(time_build(HashMap, movies))
        trie_build_times.append(time_build(Trie, movies))
        hm_exact_times.append(time_exact_hashmap(movies))
        linear_exact_times.append(time_exact_linear(movies))
        trie_prefix_times.append(time_prefix_trie(movies, PREFIX))
        linear_prefix_times.append(time_prefix_linear(movies, PREFIX))
        print(" done")

    print("\nPlotting results...\n")

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle("Hash Map vs Trie — Performance Benchmark (MovieLens)", fontsize=14)

    # Plot 1: Insertion / build time
    axes[0].plot(SIZES, hm_build_times, marker='o', label="HashMap")
    axes[0].plot(SIZES, trie_build_times, marker='s', label="Trie")
    axes[0].set_title("Insertion / Build Time")
    axes[0].set_xlabel("Dataset Size (n)")
    axes[0].set_ylabel("Average Time (seconds)")
    axes[0].legend()
    axes[0].grid(True)

    # Plot 2: Exact search time per query
    axes[1].plot(SIZES, hm_exact_times, marker='o', label="HashMap (O(1))")
    axes[1].plot(SIZES, linear_exact_times, marker='^', label="Linear Scan (O(n))")
    axes[1].set_title("Exact Search Time per Query")
    axes[1].set_xlabel("Dataset Size (n)")
    axes[1].set_ylabel("Average Time per Query (seconds)")
    axes[1].legend()
    axes[1].grid(True)

    # Plot 3: Prefix search time
    axes[2].plot(SIZES, trie_prefix_times, marker='s', label=f"Trie prefix='{PREFIX}' (O(k))")
    axes[2].plot(SIZES, linear_prefix_times, marker='^', label="Linear Scan (O(n))")
    axes[2].set_title(f"Prefix Search Time (prefix='{PREFIX}')")
    axes[2].set_xlabel("Dataset Size (n)")
    axes[2].set_ylabel("Average Time (seconds)")
    axes[2].legend()
    axes[2].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
