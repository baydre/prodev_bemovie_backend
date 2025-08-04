from django.core.cache import cache
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import MovieSerializer
from .services import TMDbService


class TrendingMoviesView(APIView):
    @extend_schema(
        responses={200: MovieSerializer(many=True)},
        description="Get trending movies from TMDb",
    )
    def get(self, request: Request) -> Response:
        cache_key = "trending_movies"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        data = TMDbService.get_trending_movies()
        if data and "results" in data:
            serializer = MovieSerializer(data["results"], many=True)
            # Cache for 15 minutes (900 seconds)
            cache.set(cache_key, serializer.data, 900)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Could not retrieve trending movies."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class MovieDetailView(APIView):
    @extend_schema(
        responses={200: MovieSerializer, 404: OpenApiTypes.OBJECT},
        description="Get detailed information for a specific movie",
    )
    def get(self, request: Request, movie_id: int) -> Response:
        cache_key = f"movie_detail_{movie_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        data = TMDbService.get_movie_details(movie_id)
        if data:
            serializer = MovieSerializer(data)
            cache.set(cache_key, serializer.data, 3600)  # Cache for 1 hour
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Movie not found or could not retrieve details."},
            status=status.HTTP_404_NOT_FOUND,
        )


class MovieRecommendationsView(APIView):
    @extend_schema(
        responses={200: MovieSerializer(many=True), 404: OpenApiTypes.OBJECT},
        description="Get movie recommendations based on a specific movie",
    )
    def get(self, request: Request, movie_id: int) -> Response:
        cache_key = f"movie_recommendations_{movie_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        data = TMDbService.get_movie_recommendations(movie_id)
        if data and "results" in data:
            serializer = MovieSerializer(data["results"], many=True)
            cache.set(cache_key, serializer.data, 900)  # Cache for 15 minutes
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Could not retrieve recommendations for this movie."},
            status=status.HTTP_404_NOT_FOUND,
        )


class MovieSearchView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="q",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search query for movies",
                required=True,
            ),
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page number for pagination",
                required=False,
            ),
        ],
        responses={200: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT},
        description="Search for movies by title",
    )
    def get(self, request: Request) -> Response:
        query = request.query_params.get("q")
        page = request.query_params.get("page", 1)

        if not query:
            return Response(
                {"detail": "Search query parameter 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cache_key = f"movie_search_{query}_{page}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        data = TMDbService.search_movies(query, page)
        if data and "results" in data:
            serializer = MovieSerializer(data["results"], many=True)
            response_data = {
                "results": serializer.data,
                "total_results": data.get("total_results", 0),
                "total_pages": data.get("total_pages", 0),
                "page": data.get("page", page),
            }
            cache.set(cache_key, response_data, 600)  # Cache for 10 minutes
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Could not perform search."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
