from abc import ABC, abstractmethod


class Searcher(ABC):

    @abstractmethod
    def insert(self, key: str, value) -> None:
        pass

    @abstractmethod
    def search(self, key: str):
        pass
