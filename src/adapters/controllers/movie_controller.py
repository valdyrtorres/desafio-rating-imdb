from fastapi import APIRouter, HTTPException
from src.application.services.movie_service import MovieService
from src.adapters.dtos.movie_dto import CreateMovieRequestDTO, MovieDTO, ReviewDTO, ActorDTO
from src.adapters.dtos.search_dto import SearchMovieRequestDTO

router = APIRouter()

class MovieController:
    def __init__(self, movie_service: MovieService):
        self.movie_service = movie_service
        self.router = router
        self.register_routes()

    def register_routes(self):
        @self.router.post("/create-movie")
        async def create_movie(request: CreateMovieRequestDTO) -> MovieDTO:
            try:
                movie = await self.movie_service.create_movie_review(
                    imdb_id=request.imdb_id,
                    user_opinion=request.user_opinion,
                    user_rating=request.user_rating
                )
                return MovieDTO(
                    imdb_id=movie.imdb_id,
                    title=movie.title,
                    year=movie.year,
                    genre=movie.genre,
                    director=movie.director,
                    actors=[ActorDTO(name=actor) for actor in movie.actors],
                    imdb_rating=movie.imdb_rating,
                    plot=movie.plot,
                    reviews=[ReviewDTO(user_opinion=review.user_opinion, user_rating=review.user_rating) for review in movie.reviews]
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))

        @self.router.get("/search-movie")
        async def search_movie(title: str = None, year: int = None) -> list[MovieDTO]:
            movies = await self.movie_service.search_movies(title=title, year=year)
            return [
                MovieDTO(
                    imdb_id=movie.imdb_id,
                    title=movie.title,
                    year=movie.year,
                    genre=movie.genre,
                    director=movie.director,
                    actors=[ActorDTO(name=actor) for actor in movie.actors],
                    imdb_rating=movie.imdb_rating,
                    plot=movie.plot,
                    reviews=[ReviewDTO(user_opinion=review.user_opinion, user_rating=review.user_rating) for review in movie.reviews]
                ) for movie in movies
            ]