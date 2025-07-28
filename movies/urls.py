from django.urls import path
from .views import TrendingMoviesView, MovieDetailView, MovieRecommendationsView

urlpatterns = [
    path('movies/trending/', TrendingMoviesView.as_view(), name='trending-movies'),
    path('movies/<int:movie_id>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/<int:movie_id>/recommendations/', MovieRecommendationsView.as_view(), name='movie-recommendations'),
]
