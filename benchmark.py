import random
import time

from data_loader.data_loader import DataLoader
from sorter.hash import HashMap, HashMapID
from sorter.trie import Trie


RUNS = 3
SIZES = [500, 1000, 2000, 4000, 8000]
PREFIXES = ["the", "star", "inc", "to"]


# ──────────────────────────────────────────────────────────────────────────────
# Insertion benchmarks
# ──────────────────────────────────────────────────────────────────────────────

def time_insert_hashmap(movies, runs=RUNS):
    """Titles into HashMap, IDs into HashMapID — two separate maps."""
    total = 0
    for _ in range(runs):
        hm_title = HashMap()
        hm_id = HashMapID()
        start = time.perf_counter()
        for movie in movies:
            hm_title.insert(movie.title.lower(), movie)
            hm_id.insert(movie.movie_id, movie)
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


# ──────────────────────────────────────────────────────────────────────────────
# Exact search benchmarks
# ──────────────────────────────────────────────────────────────────────────────

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


def time_exact_search_linear_positional(movies, position: str, runs=RUNS):
    """
    Benchmark linear scan with queries sampled from a specific position
    in the list: 'beginning' (first 10), 'middle' (centre 10), 'end' (last 10).
    This exposes how position in the list drives linear scan cost.
    """
    n = len(movies)
    if position == 'beginning':
        queries = [m.title.lower() for m in movies[:10]]
    elif position == 'middle':
        mid = n // 2
        queries = [m.title.lower() for m in movies[mid - 5: mid + 5]]
    else:  # 'end'
        queries = [m.title.lower() for m in movies[-10:]]

    total = 0
    for _ in range(runs):
        start = time.perf_counter()
        for q in queries:
            for m in movies:
                if m.title.lower() == q:
                    break
        total += time.perf_counter() - start
    return (total / runs) / len(queries)


# ──────────────────────────────────────────────────────────────────────────────
# Prefix search benchmarks
# ──────────────────────────────────────────────────────────────────────────────

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


# ──────────────────────────────────────────────────────────────────────────────
# Full-dataset mixed real + fake query benchmark
# ──────────────────────────────────────────────────────────────────────────────

def time_search_full_mixed(movies, num_real: int = 50, num_fake: int = 50, runs=RUNS):
    """
    Load all movies into HashMap and HashMapID, then search for a mix of:
      - num_real randomly sampled real titles (present in the dataset)
      - num_fake synthetic titles guaranteed not to be in the dataset

    This gives an unbiased view of HashMap vs linear scan on a realistic workload.
    Returns (hm_avg_per_query, linear_avg_per_query, hm_load_factor, hm_id_load_factor).
    """
    random.seed(42)
    real_queries = [
        m.title.lower()
        for m in random.sample(movies, min(num_real, len(movies)))
    ]
    fake_queries = [f"zzz_fake_title_{i:04d}_not_in_db" for i in range(num_fake)]
    all_queries = real_queries + fake_queries
    random.shuffle(all_queries)

    # Build structures once
    hm = HashMap()
    hm_id = HashMapID()
    for movie in movies:
        hm.insert(movie.title.lower(), movie)
        hm_id.insert(movie.movie_id, movie)

    # HashMap search
    hm_total = 0
    for _ in range(runs):
        start = time.perf_counter()
        for q in all_queries:
            hm.search(q)
        hm_total += time.perf_counter() - start
    hm_avg = (hm_total / runs) / len(all_queries)

    # Linear scan
    ln_total = 0
    for _ in range(runs):
        start = time.perf_counter()
        for q in all_queries:
            for m in movies:
                if m.title.lower() == q:
                    break
        ln_total += time.perf_counter() - start
    ln_avg = (ln_total / runs) / len(all_queries)

    return hm_avg, ln_avg, hm.load_factor(), hm_id.load_factor()


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    loader = DataLoader("data/movies.csv")
    all_movies = loader.get_all_data()

    # ------------------------------------------------------------------
    # Insertion benchmarks (scaling)
    # ------------------------------------------------------------------
    print("=== Insertion Time (avg of 3 runs, seconds) ===")
    header = f"{'Size':<8}{'HashMap+HashMapID':<22}{'Trie':<18}"
    print(header)
    print("-" * len(header))
    for size in SIZES:
        movies = loader.get_data_by_size(size)
        hm_t = time_insert_hashmap(movies)
        tr_t = time_insert_trie(movies)
        print(f"{size:<8}{hm_t:<22.6f}{tr_t:<18.6f}")

    print()

    # ------------------------------------------------------------------
    # Load factor report (full dataset)
    # ------------------------------------------------------------------
    print(f"=== Load Factor Analysis — Full Dataset ({len(all_movies):,} movies) ===")
    hm_lf_demo = HashMap()
    hm_id_lf_demo = HashMapID()
    for movie in all_movies:
        hm_lf_demo.insert(movie.title.lower(), movie)
        hm_id_lf_demo.insert(movie.movie_id, movie)
    print(f"HashMap  (titles) — capacity: {hm_lf_demo._capacity:,}  "
          f"entries: {hm_lf_demo.size():,}  load factor: {hm_lf_demo.load_factor():.4f}")
    print(f"HashMapID (IDs)   — capacity: {hm_id_lf_demo._capacity:,}  "
          f"entries: {hm_id_lf_demo.size():,}  load factor: {hm_id_lf_demo.load_factor():.4f}")
    print()

    # ------------------------------------------------------------------
    # Exact search benchmarks (scaling)
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
    # Positional linear scan (full dataset)
    # ------------------------------------------------------------------
    print(f"=== Positional Exact Search — Linear Scan (n={len(all_movies):,}) ===")
    header = f"{'Position':<15}{'HashMap Avg/query (s)':<26}{'Linear Scan Avg/query (s)':<28}"
    print(header)
    print("-" * len(header))
    hm_full = HashMap()
    for movie in all_movies:
        hm_full.insert(movie.title.lower(), movie)
    for pos in ['beginning', 'middle', 'end']:
        ln_t = time_exact_search_linear_positional(all_movies, pos)
        # HashMap is position-independent; reuse the same measurement
        hm_t = time_exact_search_hashmap(all_movies)
        print(f"{pos:<15}{hm_t:<26.8f}{ln_t:<28.8f}")

    print()

    # ------------------------------------------------------------------
    # Full-dataset mixed real + fake query benchmark
    # ------------------------------------------------------------------
    print(f"=== Full Dataset Mixed Queries (50 real + 50 fake) n={len(all_movies):,} ===")
    hm_avg, ln_avg, hm_lf, hm_id_lf = time_search_full_mixed(all_movies)
    print(f"HashMap avg/query (s):      {hm_avg:.8f}")
    print(f"Linear scan avg/query (s):  {ln_avg:.8f}")
    speedup = ln_avg / hm_avg if hm_avg > 0 else float('inf')
    print(f"Speedup (HashMap vs linear): {speedup:.1f}x")
    print(f"HashMap load factor:        {hm_lf:.4f}")
    print(f"HashMapID load factor:      {hm_id_lf:.4f}")

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
