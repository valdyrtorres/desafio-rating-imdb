from pydantic import BaseModel
from typing import List, Optional

class ReviewDTO(BaseModel):
    user_opinion: str
    user_rating: int

class ActorDTO(BaseModel):
    name: str

class MovieDTO(BaseModel):
    imdb_id: str
    title: str
    year: int
    genre: str
    director: str
    actors: List[ActorDTO]
    imdb_rating: str
    plot: str
    reviews: List[ReviewDTO]

class CreateMovieRequestDTO(BaseModel):
    imdb_id: str
    user_opinion: str
    user_rating: int