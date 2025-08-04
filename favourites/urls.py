from django.urls import path

from .views import FavoriteMovieDetailView, FavoriteMovieListView

urlpatterns = [
    path("", FavoriteMovieListView.as_view(), name="favorite-movie-list"),
    path(
        "<int:pk>/",
        FavoriteMovieDetailView.as_view(),
        name="favorite-movie-detail",
    ),
]
