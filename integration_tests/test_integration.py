from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from favourites.models import FavoriteMovie
from movies.services import TMDbService


class IntegrationTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("token_obtain_pair")
        self.favorite_list_url = reverse("favorite-movie-list")
        self.movie_recommendations_url = lambda movie_id: reverse(
            "movie-recommendations", kwargs={"movie_id": movie_id}
        )

        # Test user data
        self.user_data = {
            "username": "integrationuser",
            "email": "integration@example.com",
            "password": "strongpassword123",
        }

        # Mock responses
        self.mock_movie_data = {
            "id": 1,
            "title": "Inception",
            "overview": "A mind-bending thriller.",
            "poster_path": "/inception.jpg",
        }

    def test_full_workflow(self):
        # Step 1: Register a new user
        response = self.client.post(
            self.register_url,
            {
                "username": self.user_data["username"],
                "email": self.user_data["email"],
                "password": self.user_data["password"],
                "password2": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Fetch the JWT token
        response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Step 2: Add a movie to favorites
        with patch.object(
            TMDbService, "get_movie_details", return_value=self.mock_movie_data
        ):
            response = self.client.post(
                self.favorite_list_url, {"movie_id": self.mock_movie_data["id"]}
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # Ensure the movie is added to favorites
            self.assertTrue(
                FavoriteMovie.objects.filter(
                    user__username="integrationuser", movie_id=1
                ).exists()
            )

        # Step 3: List favorite movies
        response = self.client.get(self.favorite_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Step 4: Fetch movie recommendations
        with patch.object(
            TMDbService,
            "get_movie_recommendations",
            return_value={"results": [self.mock_movie_data]},
        ):
            response = self.client.get(self.movie_recommendations_url(1))  # Movie ID
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data[0]["title"], "Inception")
