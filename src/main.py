from fastapi import FastAPI
from src.adapters.controllers.movie_controller import MovieController
from src.application.services.movie_service import MovieService
from src.adapters.gateways.omdb_api import OmdbApiGateway
from src.adapters.gateways.movie_repository import MovieRepository
from src.infrastructure.database.init_db import init_db, get_session
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

app = FastAPI()

# Inicializar banco de dados
@app.on_event("startup")
async def startup_event():
    await init_db()

# Dependências
omdb_api = OmdbApiGateway(api_key=os.getenv("OMDB_API_KEY"))
session_factory = get_session()
movie_repository = MovieRepository(session_factory=session_factory)  # Corrigido: passa session_factory
movie_service = MovieService(movie_repository=movie_repository, omdb_api=omdb_api)
movie_controller = MovieController(movie_service=movie_service)

app.include_router(movie_controller.router)

# Fechar sessão ao encerrar
@app.on_event("shutdown")
async def shutdown_event():
    await session_factory().close_all()