from src.domain.entities.movie import Movie

class OmdbACL:
    def __init__(self, omdb_client):
        self.omdb_client = omdb_client

    async def get_movie(self, imdb_id):
        # Chama a API externa
        external_data = await self.omdb_client.fetch_movie_data(imdb_id)
        
        # Verifica se a resposta é válida
        if external_data.get("Response") == "False":
            raise ValueError(f"Filme não encontrado: {external_data.get('Error')}")

        # Mapeia os dados externos para a entidade interna
        return Movie(
            imdb_id=imdb_id,  # Adiciona o imdb_id
            title=external_data["Title"],
            year=external_data["Year"],
            genre=external_data["Genre"],
            director=external_data["Director"],
            actors=external_data["Actors"],
            imdb_rating=external_data["imdbRating"],
            plot=external_data["Plot"]
        )