from sorter.searcher_adt import Searcher


class TrieNode:
    """A single node in the Trie."""

    __slots__ = ("children", "movies", "is_end")

    def __init__(self):
        self.children: dict = {}
        self.movies: list = []
        self.is_end: bool = False


class Trie(Searcher):
    """
    Prefix Tree (Trie) implemented from scratch.

    Movie titles are inserted character by character (lowercase).
    Each terminal node stores the list of Movie objects whose title ends there.
    Prefix search traverses to the prefix node then collects all movies in the subtree.

    Time complexity:
        - insert      : O(k)  where k = len(title)
        - search      : O(k)  exact title lookup
        - prefix_search: O(k + m)  where m = number of matching results
    """

    def __init__(self):
        self._root = TrieNode()
        self._size = 0

    # ------------------------------------------------------------------
    # Public interface (Searcher ADT)
    # ------------------------------------------------------------------

    def insert(self, key: str, value) -> None:
        """Insert a movie under its (lowercase) title key."""
        node = self._root
        for ch in key:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
        node.movies.append(value)
        self._size += 1

    def search(self, key: str):
        """
        Exact title lookup. Returns the first Movie stored at this key,
        or None if the key is not present.
        """
        node = self._traverse(key)
        if node and node.is_end and node.movies:
            return node.movies[0]
        return None

    # ------------------------------------------------------------------
    # Prefix search
    # ------------------------------------------------------------------

    def prefix_search(self, prefix: str) -> list:
        """
        Return all movies whose lowercase title starts with *prefix*.
        Complexity: O(k + m) where k = len(prefix), m = matching movies.
        """
        node = self._traverse(prefix)
        if node is None:
            return []
        results = []
        self._collect(node, results)
        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _traverse(self, key: str):
        """Walk the trie along *key*; return the final node or None."""
        node = self._root
        for ch in key:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def _collect(self, node: TrieNode, results: list) -> None:
        """DFS from *node*, appending every stored movie to *results*."""
        if node.is_end:
            results.extend(node.movies)
        for child in node.children.values():
            self._collect(child, results)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"Trie(size={self._size})"
