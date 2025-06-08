# Movie API

API para gerenciamento de avaliações de filmes, integrada com a OMDb API.

## Pré-requisitos
- Docker
- Docker Compose
- Chave da OMDb API (obtenha em http://www.omdbapi.com/)

## Configuração
1. Crie um arquivo `.env` com as variáveis:
 OMDB_API_KEY=your_omdb_api_key
DATABASE_URL=postgresql://user:password@db:5432/movie_db

2. Execute:
```bash
docker-compose up --build

Endpoints
POST http://localhost:90/create-movie/ - Cria uma avaliação de filme.

GET http://localhost:90/search-movie/ - Busca filmes por título e/ou ano.


Testes
Execute os testes com:
bash

pytest tests/

