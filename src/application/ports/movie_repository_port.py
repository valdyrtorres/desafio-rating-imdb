from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.movie import Movie

class MovieRepositoryPort(ABC):
    @abstractmethod
    async def save(self, movie: Movie) -> None:
        pass

    @abstractmethod
    async def find_by_imdb_id(self, imdb_id: str) -> Optional[Movie]:
        pass

    @abstractmethod
    async def search(self, title: Optional[str] = None, year: Optional[int] = None) -> List[Movie]:
        pass