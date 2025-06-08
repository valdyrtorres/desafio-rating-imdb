from sqlalchemy import Column, Integer, String, Float, ARRAY, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class MovieModel(Base):
    __tablename__ = "movies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    imdb_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    director = Column(String, nullable=False)
    actors = Column(ARRAY(String), nullable=False)
    imdb_rating = Column(String, nullable=False)
    plot = Column(String, nullable=False)

class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id"), nullable=False)
    user_opinion = Column(String, nullable=False)
    user_rating = Column(Integer, nullable=False)