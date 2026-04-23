from sorter.searcher_adt import Searcher


class HashMap(Searcher):
    """
    Hash Map implemented from scratch using separate chaining for collision resolution.

    Each bucket holds a list of (key, value) pairs. The hash function is a
    polynomial rolling hash (djb2-style) applied to string keys.

    Average-case time complexity:
        - insert : O(1)
        - search : O(1)
    Worst-case (all keys collide): O(n)
    """

    DEFAULT_CAPACITY = 1024

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
