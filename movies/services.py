import logging
from typing import Any, Dict, Optional, Union

import requests
from django.conf import settings


class TMDbService:
    """
    Service class for interacting with The Movie Database (TMDb) API.

    Provides methods to fetch trending movies, movie details, recommendations,
    and search functionality with proper error handling and logging.
    """

    BASE_URL = "https://api.themoviedb.org/3"
    API_KEY = settings.TMDB_API_KEY

    logger = logging.getLogger(__name__)

    @classmethod
    def _make_request(
        cls, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request to TMDb API with error handling and logging.

        Args:
            endpoint: API endpoint path
            params: Optional query parameters

        Returns:
            JSON response data or None if request fails
        """
        params = params or {}
        params["api_key"] = cls.API_KEY
        try:
            response = requests.get(f"{cls.BASE_URL}/{endpoint}", params=params)
            # Raise HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            cls.logger.error(
                f"HTTP error occurred: {http_err} - Response: {response.text}",
                extra={
                    "endpoint": endpoint,
                    "params": params,
                    "status_code": response.status_code,
                },
            )
            return None
        except requests.exceptions.ConnectionError as conn_err:
            cls.logger.error(
                f"Connection error occurred: {conn_err}",
                extra={"endpoint": endpoint, "params": params},
            )
            return None
        except requests.exceptions.Timeout as timeout_err:
            cls.logger.warning(
                f"Timeout error occurred: {timeout_err}",
                extra={"endpoint": endpoint, "params": params},
            )
            return None
        except requests.exceptions.RequestException as req_err:
            cls.logger.error(
                f"Request error occurred: {req_err}",
                extra={"endpoint": endpoint, "params": params},
            )
            return None

    @classmethod
    def get_trending_movies(
        cls, time_window: str = "week", page: int = 1
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch trending movies from TMDb.

        Args:
            time_window: Time window for trending ('day' or 'week')
            page: Page number for pagination

        Returns:
            Dictionary containing trending movies data
        """
        return cls._make_request(f"trending/movie/{time_window}", {"page": page})

    @classmethod
    def get_movie_details(cls, movie_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """
        Fetch detailed information for a specific movie.

        Args:
            movie_id: TMDb movie ID

        Returns:
            Dictionary containing movie details
        """
        return cls._make_request(f"movie/{movie_id}")

    @classmethod
    def get_movie_recommendations(
        cls, movie_id: Union[int, str], page: int = 1
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch movie recommendations based on a specific movie.

        Args:
            movie_id: TMDb movie ID to base recommendations on
            page: Page number for pagination

        Returns:
            Dictionary containing recommended movies
        """
        return cls._make_request(f"movie/{movie_id}/recommendations", {"page": page})

    @classmethod
    def search_movies(cls, query: str, page: int = 1) -> Optional[Dict[str, Any]]:
        """
        Search for movies by title.

        Args:
            query: Search query string
            page: Page number for pagination

        Returns:
            Dictionary containing search results
        """
        return cls._make_request("search/movie", {"query": query, "page": page})
