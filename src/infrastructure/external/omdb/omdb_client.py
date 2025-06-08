import aiohttp

class OmdbClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://www.omdbapi.com/"

    async def fetch_movie_data(self, imdb_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}?i={imdb_id}&apikey={self.api_key}") as response:
                return await response.json()