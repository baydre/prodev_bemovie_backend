from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from movies.services import TMDbService

from .models import FavoriteMovie


class FavoriteMovieAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

        # Get JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.list_create_url = reverse("favorite-movie-list")
        self.detail_url = reverse("favorite-movie-detail", kwargs={"pk": 1})

        self.mock_movie_data = {
            "id": 1,
            "title": "Test Movie",
            "overview": "A test movie",
            "poster_path": "/test.jpg",
        }

    @patch.object(TMDbService, "get_movie_details")
    def test_add_favorite_movie(self, mock_get_details):
        mock_get_details.return_value = self.mock_movie_data

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post(self.list_create_url, {"movie_id": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            FavoriteMovie.objects.filter(user=self.user, movie_id=1).exists()
        )

    def test_add_favorite_movie_unauthenticated(self):
        response = self.client.post(self.list_create_url, {"movie_id": 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch.object(TMDbService, "get_movie_details")
    def test_add_duplicate_favorite_movie(self, mock_get_details):
        mock_get_details.return_value = self.mock_movie_data

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.client.post(self.list_create_url, {"movie_id": 1})  # Add first time
        response = self.client.post(
            self.list_create_url, {"movie_id": 1}
        )  # Try adding again
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_delete_favorite_movie(self):
        favorite = FavoriteMovie.objects.create(
            user=self.user, movie_id=1, title="Test Movie"
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FavoriteMovie.objects.filter(pk=favorite.pk).exists())

    def test_list_favorite_movies(self):
        FavoriteMovie.objects.create(user=self.user, movie_id=1, title="Test Movie")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
