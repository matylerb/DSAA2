# Movie Search — HashMap & Trie

A Python project that implements and benchmarks two custom data structures (HashMap and Trie) on a MovieLens dataset, with an interactive menu, automated benchmarking, data exploration, and performance visualisation.

## Features

- **2 Data Structures**: HashMap (exact title/ID search) and Trie (prefix/autocomplete search) — each implementing a common `Searcher` abstract base class
- **Performance Benchmarking**: Compare build times and search times across multiple data sizes (500–8 000 records), averaged over multiple runs
- **Visualisation**: Matplotlib charts plotting time vs. data size for both structures
- **Data Exploration**: ydata-profiling HTML report of the MovieLens dataset — [matylerb.ie/movies_report.html](https://matylerb.ie/movies_report.html)
- **CSV Export**: Prefix search results written to the `output/` directory
- **Multiple Entry Points**: Interactive menu, automated benchmarking, and demo script

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/matylerb/DSAA.git
cd assignment2/DSAA2
```

### 2. Set Up Virtual Environment (Windows)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Configure VS Code (Optional)

1. Press `Ctrl + Shift + P`
2. Type `Python: Select Interpreter`
3. Choose `.venv\Scripts\python.exe`

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Key dependencies: `matplotlib`, `numpy`, `pandas`, `ydata-profiling` (see `requirements.txt` for the full list).

## Usage

| Script | Description |
|--------|-------------|
| `python main.py` | Demo: build HashMap & Trie, run sample exact/prefix searches, export results to `output/` |
| `python main_menu.py` | Interactive menu: exact search by title or ID, prefix autocomplete, rebuild with different dataset size |
| `python main_tester.py` | Benchmark build and search times across sizes, plots results with Matplotlib |
| `python benchmark.py` | Extended benchmarking utilities for insertion and search timing |
| `python exploration.py` | Generates `movies_report.html` — full ydata-profiling report of the dataset |

## Project Structure

```
DSAA2/
├── main.py               # Demo: HashMap & Trie searches, exports prefix results to output/
├── main_menu.py          # Interactive menu-driven interface
├── main_tester.py        # Benchmark with Matplotlib charts
├── benchmark.py          # Extended benchmarking utilities
├── exploration.py        # ydata-profiling HTML data exploration report
├── requirements.txt      # Python dependencies
├── business/
│   └── movie_collection.py  # MovieCollection: builds structures, delegates searches
├── data_loader/
│   └── data_loader.py    # DataLoader: CSV → Movie objects, supports load-by-size
├── model/
│   └── movies.py         # Movie model class (movie_id, title, genres)
├── sorter/
│   ├── searcher_adt.py   # Searcher abstract base class
│   ├── hash.py           # HashMap (djb2 hash, separate chaining) + HashMapID
│   └── trie.py           # Trie (character-level prefix tree)
├── data/
│   └── movies.csv        # MovieLens dataset (~87 585 movies)
└── output/               # Generated CSV files (e.g. prefix_search_the.csv)
```