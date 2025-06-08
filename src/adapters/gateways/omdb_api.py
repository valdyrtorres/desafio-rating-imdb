import requests
from typing import Optional, Dict, Any
from src.application.ports.omdb_api_port import OmdbApiPort

class OmdbApiGateway(OmdbApiPort):
    def __init__(self, api_key: str):
        self.base_url = "http://www.omdbapi.com/"
        self.api_key = api_key

    async def fetch_movie_data(self, imdb_id: str) -> Optional[Dict[str, Any]]:
        params = {"i": imdb_id, "apikey": self.api_key}
        response = requests.get(self.base_url, params=params)
        if response.status_code != 200 or response.json().get("Response") == "False":
            return None
        return response.json()