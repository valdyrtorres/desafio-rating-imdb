from typing import List, Optional
from src.domain.entities.movie import Movie
from src.domain.value_objects.review import Review
from src.application.ports.movie_repository_port import MovieRepositoryPort
from src.application.ports.omdb_api_port import OmdbApiPort

class MovieService:
    def __init__(self, movie_repository: MovieRepositoryPort, omdb_api: OmdbApiPort):
        self.movie_repository = movie_repository
        self.omdb_api = omdb_api

    async def create_movie_review(self, imdb_id: str, user_opinion: str, user_rating: int) -> Movie:
        movie = await self.movie_repository.find_by_imdb_id(imdb_id)
        review = Review(user_opinion=user_opinion, user_rating=user_rating)

        if not movie:
            omdb_data = await self.omdb_api.fetch_movie_data(imdb_id)
            if not omdb_data:
                raise ValueError("Movie not found in OMDb API")
            
            movie = Movie(
                imdb_id=imdb_id,
                title=omdb_data["Title"],
                year=int(omdb_data["Year"]),
                genre=omdb_data["Genre"],
                director=omdb_data["Director"],
                actors=omdb_data["Actors"].split(", "),
                imdb_rating=omdb_data["imdbRating"],
                plot=omdb_data["Plot"]
            )

        movie.add_review(review)
        await self.movie_repository.save(movie)
        return movie

    async def search_movies(self, title: Optional[str] = None, year: Optional[int] = None) -> List[Movie]:
        return await self.movie_repository.search(title, year)