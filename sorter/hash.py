from sorter.searcher_adt import Searcher


class HashMap(Searcher):
    """
    Hash Map implemented from scratch using separate chaining for collision resolution.

    Each bucket holds a list of (key, value) pairs. The hash function is a
    polynomial rolling hash (djb2-style) applied to string keys.

    Capacity is set to 131,072 (2^17) so that the load factor stays at or
    below 0.75 for the full 87,585-movie dataset.

    Average-case time complexity:
        - insert : O(1)
        - search : O(1)
    Worst-case (all keys collide): O(n)
    """

    DEFAULT_CAPACITY = 131072  # 2^17 — keeps LF ≤ 0.75 for up to ~98k title keys

    def __init__(self, capacity=DEFAULT_CAPACITY):
        self._capacity = capacity
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _hash(self, key: str) -> int:
        """djb2 polynomial rolling hash."""
        h = 5381
        for ch in key:
            h = ((h << 5) + h) + ord(ch)
        return h % self._capacity

    # ------------------------------------------------------------------
    # Public interface (Searcher ADT)
    # ------------------------------------------------------------------

    def insert(self, key: str, value) -> None:
        """Insert or update a key-value pair."""
        index = self._hash(key)
        bucket = self._buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def search(self, key: str):
        """Return the value associated with key, or None if not found."""
        index = self._hash(key)
        for k, v in self._buckets[index]:
            if k == key:
                return v
        return None

    # ------------------------------------------------------------------
    # Additional utilities
    # ------------------------------------------------------------------

    def delete(self, key: str) -> bool:
        """Remove a key-value pair. Returns True if removed, False if not found."""
        index = self._hash(key)
        bucket = self._buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def size(self) -> int:
        return self._size

    def load_factor(self) -> float:
        return self._size / self._capacity

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"HashMap(size={self._size}, capacity={self._capacity}, load={self.load_factor():.2f})"


class HashMapID:
    """
    Dedicated hash map for integer movie IDs using separate chaining.

    Uses Knuth multiplicative hashing, which distributes sparse integer keys
    (such as MovieLens IDs) far more uniformly than treating the digits as a
    string and running djb2.  Keeping this map separate from the title HashMap
    means each map only stores one entry per movie, keeping both load factors
    at or below 0.75 for the full 87,585-movie dataset.

    Average-case time complexity:
        - insert : O(1)
        - search : O(1)
    Worst-case (all keys collide): O(n)
    """

    DEFAULT_CAPACITY = 131072  # 2^17 — LF ≈ 0.668 for 87,585 movies

    def __init__(self, capacity: int = DEFAULT_CAPACITY):
        self._capacity = capacity
        self._buckets: list = [[] for _ in range(self._capacity)]
        self._size = 0

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _hash(self, key: int) -> int:
        """Knuth multiplicative hash for integer keys."""
        return (key * 2654435761) % self._capacity

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def insert(self, key: int, value) -> None:
        """Insert or update a key-value pair."""
        index = self._hash(key)
        bucket = self._buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def search(self, key: int):
        """Return the value associated with key, or None if not found."""
        index = self._hash(key)
        for k, v in self._buckets[index]:
            if k == key:
                return v
        return None

    def delete(self, key: int) -> bool:
        """Remove a key-value pair. Returns True if removed, False if not found."""
        index = self._hash(key)
        bucket = self._buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def size(self) -> int:
        return self._size

    def load_factor(self) -> float:
        return self._size / self._capacity

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"HashMapID(size={self._size}, capacity={self._capacity}, load={self.load_factor():.2f})"
