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

ou 
POST http://architecture-test:90/create-movie/ - Cria uma avaliação de filme.

GET http://architecture-test:90/search-movie/ - Busca filmes por título e/ou ano.
OBS: Criar entrada architecture-test para 127.0.0.1 no arquivo de hosts


Testes
Execute os testes com:
bash

pytest tests/ ou
docker-compose run --rm test

Se os testes falharem, você pode inspecionar o ambiente:
docker-compose run --rm test bash

pytest tests/ --verbose
docker-compose logs test

NOTA: Camada anticorrupção (ACL)
diretório src/infrastructure/external

- Procurar filme
curl --location 'http://architecture-test:90/search-movie?title=Inception&year=2010' \
--data ''

- Criar rating
curl --location 'http://architecture-test:90/create-movie' \
--header 'Content-Type: application/json' \
--data '{
"imdb_id": "tt1375666",
"user_opinion": "teste 1",
"user_rating": 5
}'

NOTA IMPORTANTE: Para responder para o domínio architecture-test, criar uma entrada no arquivo de hosts para 127.0.0.1 tipo:
127.0.0.1 architecture-test


