from src.domain.entities.movie import Movie
from src.infrastructure.external.omdb.omdb_acl import OmdbACL

class MovieService:
    def __init__(self, movie_repository, omdb_acl: OmdbACL):
        self.movie_repository = movie_repository
        self.omdb_acl = omdb_acl

    async def create_movie_review(self, imdb_id, user_opinion, user_rating):
        # Verifica se o filme já existe
        existing_movie = await self.movie_repository.find_by_imdb_id(imdb_id)
        if existing_movie:
            movie = existing_movie
        else:
            # Usa a ACL para obter e traduzir os dados do filme
            movie = await self.omdb_acl.get_movie(imdb_id)
            await self.movie_repository.save(movie)

        # Adiciona a review
        movie.reviews.append({"user_opinion": user_opinion, "user_rating": user_rating})
        await self.movie_repository.update(movie)
        return movie