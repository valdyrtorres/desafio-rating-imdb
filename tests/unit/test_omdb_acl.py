import pytest
from src.infrastructure.external.omdb.omdb_acl import OmdbACL
from src.domain.entities.movie import Movie
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_omdb_acl_maps_external_data_to_movie():
    # Mock do cliente OMDb
    omdb_client = AsyncMock()
    omdb_client.fetch_movie_data.return_value = {
        "Response": "True",
        "Title": "A Origem",
        "Year": "2010",
        "Genre": "Acao, Aventura, Ficcao Cientifica",
        "Director": "Christopher Nolan",
        "Actors": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "imdbRating": "8.8",
        "Plot": "Um ladrao que rouba segredos corporativos..."
    }

    # Instancia a ACL
    omdb_acl = OmdbACL(omdb_client)
    
    # Executa
    movie = await omdb_acl.get_movie("tt1375666")

    # Verificações
    assert isinstance(movie, Movie)
    assert movie.imdb_id == "tt1375666"  # Verifica o imdb_id
    assert movie.title == "A Origem"
    assert movie.year == "2010"
    assert movie.imdb_rating == "8.8"
    omdb_client.fetch_movie_data.assert_called_once_with("tt1375666")

@pytest.mark.asyncio
async def test_omdb_acl_handles_api_error():
    # Mock do cliente OMDb com erro
    omdb_client = AsyncMock()
    omdb_client.fetch_movie_data.return_value = {
        "Response": "False",
        "Error": "Movie not found!"
    }

    # Instancia a ACL
    omdb_acl = OmdbACL(omdb_client)
    
    # Verifica se a exceção é lançada
    with pytest.raises(ValueError, match="Filme não encontrado: Movie not found!"):
        await omdb_acl.get_movie("tt0000000")