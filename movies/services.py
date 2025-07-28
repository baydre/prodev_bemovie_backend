import requests
from django.conf import settings

class TMDbService:
    BASE_URL = "https://api.themoviedb.org/3"
    API_KEY = settings.TMDB_API_KEY

    @classmethod
    def _make_request(cls, endpoint, params=None):
        params = params or {}
        params['api_key'] = cls.API_KEY
        try:
            response = requests.get(f"{cls.BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - Response: {response.text}")
            # Implement robust error handling (e.g., return specific error codes, log errors)
            return None
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return None

    @classmethod
    def get_trending_movies(cls, time_window='week', page=1):
        return cls._make_request(f"trending/movie/{time_window}", {'page': page})

    @classmethod
    def get_movie_details(cls, movie_id):
        return cls._make_request(f"movie/{movie_id}")

    @classmethod
    def get_movie_recommendations(cls, movie_id, page=1):
        return cls._make_request(f"movie/{movie_id}/recommendations", {'page': page})
