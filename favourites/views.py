from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Import TMDbService from movies_data app
from movies.services import TMDbService
from .models import FavoriteMovie
from .serializers import FavoriteMovieSerializer

class FavoriteMovieListView(generics.ListCreateAPIView):
    serializer_class = FavoriteMovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only see their own favorite movies
        return self.request.user.favorite_movies.all()

    def create(self, request, *args, **kwargs):
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({"movie_id": "Movie ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch movie details from TMDb to get title and poster_path
        movie_data = TMDbService.get_movie_details(movie_id)
        if not movie_data:
            return Response({"detail": "Movie not found on TMDb."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the movie is already favorited by the user
        if FavoriteMovie.objects.filter(user=request.user, movie_id=movie_id).exists():
            return Response({"detail": "Movie already in favorites."}, status=status.HTTP_409_CONFLICT)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            title=movie_data.get('title', 'Unknown Title'),
            poster_path=movie_data.get('poster_path')
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class FavoriteMovieDetailView(generics.DestroyAPIView):
    queryset = FavoriteMovie.objects.all()
    serializer_class = FavoriteMovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only delete their own favorite movies
        return self.request.user.favorite_movies.all()
