from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache 

from .services import TMDbService
from .serializers import MovieSerializer

class TrendingMoviesView(APIView):
    def get(self, request):
        cache_key = 'trending_movies'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        data = TMDbService.get_trending_movies()
        if data and 'results' in data:
            serializer = MovieSerializer(data['results'], many=True)
            # Cache for 15 minutes (900 seconds)
            cache.set(cache_key, serializer.data, 900)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Could not retrieve trending movies."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MovieDetailView(APIView):
    def get(self, request, movie_id):
        cache_key = f'movie_detail_{movie_id}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        data = TMDbService.get_movie_details(movie_id)
        if data:
            serializer = MovieSerializer(data)
            cache.set(cache_key, serializer.data, 3600) # Cache for 1 hour
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Movie not found or could not retrieve details."}, status=status.HTTP_404_NOT_FOUND)

class MovieRecommendationsView(APIView):
    def get(self, request, movie_id):
        cache_key = f'movie_recommendations_{movie_id}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        data = TMDbService.get_movie_recommendations(movie_id)
        if data and 'results' in data:
            serializer = MovieSerializer(data['results'], many=True)
            cache.set(cache_key, serializer.data, 900) # Cache for 15 minutes
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Could not retrieve recommendations for this movie."}, status=status.HTTP_404_NOT_FOUND)
