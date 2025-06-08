from pydantic import BaseModel
from typing import Optional

class SearchMovieRequestDTO(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = None