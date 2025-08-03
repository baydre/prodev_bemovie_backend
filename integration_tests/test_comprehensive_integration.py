from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from movies.services import TMDbService
from favourites.models import FavoriteMovie

class ComprehensiveIntegrationTestCase(APITestCase):

    def setUp(self):
        # URLs
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.profile_url = reverse('user-profile')
        self.favorite_list_url = reverse('favorite-movie-list')
        self.trending_url = reverse('trending-movies')
        self.search_url = reverse('movie-search')
        
        # Test user data
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        }

        # Mock movie data
        self.mock_movie_data = {
            'id': 550,
            'title': 'Fight Club',
            'overview': 'An insomniac office worker forms a secret fight club.',
            'poster_path': '/fight_club.jpg',
            'release_date': '1999-10-15',
            'vote_average': 8.8
        }

        self.mock_trending_data = {
            'results': [
                self.mock_movie_data,
                {
                    'id': 13,
                    'title': 'Forrest Gump',
                    'overview': 'Life is like a box of chocolates.',
                    'poster_path': '/forrest_gump.jpg',
                    'release_date': '1994-07-06',
                    'vote_average': 8.8
                }
            ]
        }

    def authenticate_user(self):
        """Helper method to register and authenticate a user"""
        # Register
        self.client.post(self.register_url, {
            'username': self.user_data['username'],
            'email': self.user_data['email'],
            'password': self.user_data['password'],
            'password2': self.user_data['password']
        })
        
        # Login
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return token

    def test_end_to_end_movie_app_workflow(self):
        """Test complete workflow from registration to movie management"""
        
        # Step 1: Test public endpoints (no authentication required)
        with patch.object(TMDbService, 'get_trending_movies', return_value=self.mock_trending_data):
            response = self.client.get(self.trending_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 2)

        with patch.object(TMDbService, 'search_movies', return_value=self.mock_trending_data):
            response = self.client.get(self.search_url, {'q': 'fight'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('results', response.data)

        # Step 2: Register and authenticate
        token = self.authenticate_user()
        self.assertIsNotNone(token)

        # Step 3: Test user profile management
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])

        # Update profile
        response = self.client.patch(self.profile_url, {'email': 'updated@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'updated@example.com')

        # Step 4: Test favorites management
        # Add first favorite
        with patch.object(TMDbService, 'get_movie_details', return_value=self.mock_movie_data):
            response = self.client.post(self.favorite_list_url, {'movie_id': 550})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['title'], 'Fight Club')

        # Try to add duplicate (should fail)
        with patch.object(TMDbService, 'get_movie_details', return_value=self.mock_movie_data):
            response = self.client.post(self.favorite_list_url, {'movie_id': 550})
            self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # Add second favorite
        second_movie = {
            'id': 13,
            'title': 'Forrest Gump',
            'overview': 'Life is like a box of chocolates.',
            'poster_path': '/forrest_gump.jpg'
        }
        with patch.object(TMDbService, 'get_movie_details', return_value=second_movie):
            response = self.client.post(self.favorite_list_url, {'movie_id': 13})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # List favorites
        response = self.client.get(self.favorite_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Step 5: Test movie recommendations
        with patch.object(TMDbService, 'get_movie_recommendations', return_value=self.mock_trending_data):
            recommendations_url = reverse('movie-recommendations', kwargs={'movie_id': 550})
            response = self.client.get(recommendations_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 2)

        # Step 6: Remove a favorite
        favorite = FavoriteMovie.objects.get(user__username=self.user_data['username'], movie_id=550)
        detail_url = reverse('favorite-movie-detail', kwargs={'pk': favorite.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify it's removed
        response = self.client.get(self.favorite_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Forrest Gump')

    def test_authentication_required_endpoints(self):
        """Test that protected endpoints require authentication"""
        
        # Test favorites without authentication
        response = self.client.get(self.favorite_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(self.favorite_list_url, {'movie_id': 550})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test profile without authentication
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_error_scenarios(self):
        """Test various error scenarios"""
        
        self.authenticate_user()

        # Test adding non-existent movie to favorites
        with patch.object(TMDbService, 'get_movie_details', return_value=None):
            response = self.client.post(self.favorite_list_url, {'movie_id': 99999})
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test search without query parameter
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test accessing non-existent favorite
        response = self.client.get(reverse('favorite-movie-detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
