import pytest
from src.application.services.movie_service import MovieService
from src.domain.entities.movie import Movie
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_create_movie_review():
    movie_repository = AsyncMock()
    omdb_api = AsyncMock()
    omdb_api.fetch_movie_data.return_value = {
        "Title": "A Origem",
        "Year": "2010",
        "Genre": "Acao, Aventura, Ficcao Cientifica",
        "Director": "Christopher Nolan",
        "Actors": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "imdbRating": "8.8",
        "Plot": "Um ladrao que rouba segredos corporativos..."
    }
    movie_repository.find_by_imdb_id.return_value = None

    movie_service = MovieService(movie_repository, omdb_api)
    movie = await movie_service.create_movie_review(
        imdb_id="tt1375666",
        user_opinion="Trama excelente!",
        user_rating=9
    )

    assert movie.title == "A Origem"
    assert len(movie.reviews) == 1
    assert movie.reviews[0].user_opinion == "Trama excelente!"