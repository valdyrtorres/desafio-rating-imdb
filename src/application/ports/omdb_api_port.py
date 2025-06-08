from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class OmdbApiPort(ABC):
    @abstractmethod
    async def fetch_movie_data(self, imdb_id: str) -> Optional[Dict[str, Any]]:
        pass