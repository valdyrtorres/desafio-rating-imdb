import pytest
from src.application.services.movie_service import MovieService
from src.domain.entities.movie import Movie
from src.infrastructure.external.omdb.omdb_acl import OmdbACL
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_create_movie_review():
    # Mock do repositório
    movie_repository = AsyncMock()
    movie_repository.find_by_imdb_id.return_value = None

    # Mock da ACL
    omdb_acl = AsyncMock(spec=OmdbACL)
    omdb_acl.get_movie.return_value = Movie(
        imdb_id="tt1375666",  # Adiciona o imdb_id
        title="A Origem",
        year="2010",
        genre="Acao, Aventura, Ficcao Cientifica",
        director="Christopher Nolan",
        actors="Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        imdb_rating="8.8",
        plot="Um ladrao que rouba segredos corporativos..."
    )

    # Instancia o serviço com a ACL mockada
    movie_service = MovieService(movie_repository, omdb_acl)
    movie = await movie_service.create_movie_review(
        imdb_id="tt1375666",
        user_opinion="Trama excelente!",
        user_rating=9
    )

    # Verificações
    assert movie.title == "A Origem"
    assert len(movie.reviews) == 1
    assert movie.reviews[0]["user_opinion"] == "Trama excelente!"
    omdb_acl.get_movie.assert_called_once_with("tt1375666")
    movie_repository.save.assert_called_once()