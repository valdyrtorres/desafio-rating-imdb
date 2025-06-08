from typing import List
from src.domain.value_objects.review import Review

class Movie:
    def __init__(self, imdb_id: str, title: str, year: int, genre: str, director: str, actors: List[str], imdb_rating: str, plot: str, reviews: List[Review] = None):
        self.imdb_id = imdb_id
        self.title = title
        self.year = year
        self.genre = genre
        self.director = director
        self.actors = actors
        self.imdb_rating = imdb_rating
        self.plot = plot
        self.reviews = reviews or []

    def add_review(self, review: Review):
        self.reviews.append(review)