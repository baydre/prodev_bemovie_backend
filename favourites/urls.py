from django.urls import path
from .views import FavoriteMovieListView, FavoriteMovieDetailView

urlpatterns = [
    path('', FavoriteMovieListView.as_view(), name='favorite-movie-list'),
    path('<int:pk>/', FavoriteMovieDetailView.as_view(), name='favorite-movie-detail'),
]
