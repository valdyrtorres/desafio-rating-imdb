from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.entities.movie import Movie
from src.domain.value_objects.review import Review
from src.application.ports.movie_repository_port import MovieRepositoryPort
from src.infrastructure.database.models import MovieModel, ReviewModel

class MovieRepository(MovieRepositoryPort):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def save(self, movie: Movie) -> None:
        async with self.session_factory() as session:
            async with session.begin():
                movie_model = (
                    await session.execute(
                        select(MovieModel).filter_by(imdb_id=movie.imdb_id)
                    )
                ).scalar_one_or_none()

                if not movie_model:
                    movie_model = MovieModel(
                        imdb_id=movie.imdb_id,
                        title=movie.title,
                        year=movie.year,
                        genre=movie.genre,
                        director=movie.director,
                        actors=movie.actors,
                        imdb_rating=movie.imdb_rating,
                        plot=movie.plot
                    )
                    session.add(movie_model)
                    await session.flush()  # Garante que movie_model.id esteja disponível

                for review in movie.reviews:
                    review_model = ReviewModel(
                        movie_id=movie_model.id,
                        user_opinion=review.user_opinion,
                        user_rating=review.user_rating
                    )
                    session.add(review_model)

                await session.commit()

    async def find_by_imdb_id(self, imdb_id: str) -> Optional[Movie]:
        async with self.session_factory() as session:
            movie_model = (
                await session.execute(
                    select(MovieModel).filter_by(imdb_id=imdb_id)
                )
            ).scalar_one_or_none()

            if not movie_model:
                return None

            reviews = (
                await session.execute(
                    select(ReviewModel).filter_by(movie_id=movie_model.id)
                )
            ).scalars().all()

            return Movie(
                imdb_id=movie_model.imdb_id,
                title=movie_model.title,
                year=movie_model.year,
                genre=movie_model.genre,
                director=movie_model.director,
                actors=movie_model.actors,
                imdb_rating=movie_model.imdb_rating,
                plot=movie_model.plot,
                reviews=[
                    Review(user_opinion=r.user_opinion, user_rating=r.user_rating)
                    for r in reviews
                ]
            )

    async def search(self, title: Optional[str] = None, year: Optional[int] = None) -> List[Movie]:
        async with self.session_factory() as session:
            query = select(MovieModel)
            if title:
                query = query.filter(MovieModel.title.ilike(f"%{title}%"))
            if year:
                query = query.filter(MovieModel.year == year)

            movies = (await session.execute(query)).scalars().all()
            result = []

            for movie_model in movies:
                reviews = (
                    await session.execute(
                        select(ReviewModel).filter_by(movie_id=movie_model.id)
                    )
                ).scalars().all()

                result.append(
                    Movie(
                        imdb_id=movie_model.imdb_id,
                        title=movie_model.title,
                        year=movie_model.year,
                        genre=movie_model.genre,
                        director=movie_model.director,
                        actors=movie_model.actors,
                        imdb_rating=movie_model.imdb_rating,
                        plot=movie_model.plot,
                        reviews=[
                            Review(user_opinion=r.user_opinion, user_rating=r.user_rating)
                            for r in reviews
                        ]
                    )
                )

            return result