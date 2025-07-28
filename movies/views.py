from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import TMDbService
from .serializers import MovieSerializer
from django.core.cache import cache # For caching later

class TrendingMoviesView(APIView):
    def get(self, request):
        # We'll add caching here in the optimization phase
        data = TMDbService.get_trending_movies()
        if data and 'results' in data:
            serializer = MovieSerializer(data['results'], many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Could not retrieve trending movies."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MovieDetailView(APIView):
    def get(self, request, movie_id):
        data = TMDbService.get_movie_details(movie_id)
        if data:
            serializer = MovieSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Movie not found or could not retrieve details."}, status=status.HTTP_404_NOT_FOUND)

class MovieRecommendationsView(APIView):
    def get(self, request, movie_id):
        data = TMDbService.get_movie_recommendations(movie_id)
        if data and 'results' in data:
            serializer = MovieSerializer(data['results'], many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Could not retrieve recommendations for this movie."}, status=status.HTTP_404_NOT_FOUND)
