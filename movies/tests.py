from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch, MagicMock
from django.core.cache import cache
from .services import TMDbService

class MovieAPITestCase(APITestCase):
    def setUp(self):
        self.trending_url = reverse('trending-movies')
        self.search_url = reverse('movie-search')
        
        # Mock movie data
        self.mock_movie_data = {
            'results': [
                {
                    'id': 1,
                    'title': 'Test Movie',
                    'overview': 'A test movie',
                    'poster_path': '/test.jpg',
                    'release_date': '2023-01-01',
                    'vote_average': 8.5
                }
            ],
            'total_results': 1,
            'total_pages': 1,
            'page': 1
        }
        
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Get JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
    
    def tearDown(self):
        cache.clear()

    def test_get_trending_movies_unauthenticated(self):
        # Assuming the trending endpoint is public; this should pass
        response = self.client.get(self.trending_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    @patch.object(TMDbService, 'get_trending_movies')
    def test_trending_movies_cache(self, mock_get_trending):
        mock_get_trending.return_value = self.mock_movie_data

        # First call, should fetch from TMDb and cache
        self.client.get(self.trending_url)
        cached_data = cache.get('trending_movies')
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 1)
        self.assertEqual(cached_data[0]['title'], 'Test Movie')

        # Second call, should hit cache
        response = self.client.get(self.trending_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Movie', response.data[0]['title'])

    @patch.object(TMDbService, 'get_trending_movies')
    def test_get_trending_movies(self, mock_get_trending):
        mock_get_trending.return_value = self.mock_movie_data
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        response = self.client.get(self.trending_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Movie')
    
    @patch.object(TMDbService, 'search_movies')
    def test_search_movies(self, mock_search):
        mock_search.return_value = self.mock_movie_data
        
        response = self.client.get(self.search_url, {'q': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Test Movie')
    
    def test_search_movies_no_query(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @patch.object(TMDbService, 'get_movie_details')
    def test_get_movie_details(self, mock_get_details):
        mock_get_details.return_value = self.mock_movie_data['results'][0]
        
        movie_detail_url = reverse('movie-detail', kwargs={'movie_id': 1})
        response = self.client.get(movie_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Movie')
    
    @patch.object(TMDbService, 'get_movie_details')
    def test_get_movie_details_unauthenticated(self, mock_get_details):
        mock_get_details.return_value = self.mock_movie_data['results'][0]
        
        movie_detail_url = reverse('movie-detail', kwargs={'movie_id': 1})
        response = self.client.get(movie_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) # Assuming this is public; adjust if not
        
    @patch.object(TMDbService, 'get_movie_recommendations')
    def test_get_movie_recommendations(self, mock_get_recommendations):
        mock_get_recommendations.return_value = self.mock_movie_data
        
        recommendations_url = reverse('movie-recommendations', kwargs={'movie_id': 1})
        response = self.client.get(recommendations_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Movie')
    
    @patch.object(TMDbService, 'get_movie_details')
    def test_movie_details_cache(self, mock_get_details):
        mock_get_details.return_value = self.mock_movie_data['results'][0]
        movie_detail_url = reverse('movie-detail', kwargs={'movie_id': 1})
        
        # First call, should fetch from TMDb and cache
        response = self.client.get(movie_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if data is cached
        cached_data = cache.get('movie_detail_1')
        self.assertIsNotNone(cached_data)
        self.assertEqual(cached_data['title'], 'Test Movie')
        
        # Second call, should hit cache (mock should only be called once)
        response = self.client.get(movie_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Movie')
    
    @patch.object(TMDbService, 'get_movie_recommendations')
    def test_movie_recommendations_cache(self, mock_get_recommendations):
        mock_get_recommendations.return_value = self.mock_movie_data
        recommendations_url = reverse('movie-recommendations', kwargs={'movie_id': 1})
        
        # First call, should fetch from TMDb and cache
        response = self.client.get(recommendations_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if data is cached
        cached_data = cache.get('movie_recommendations_1')
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data), 1)
        self.assertEqual(cached_data[0]['title'], 'Test Movie')
        
        # Second call, should hit cache
        response = self.client.get(recommendations_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Movie')
    
    @patch.object(TMDbService, 'search_movies')
    def test_movie_search_cache(self, mock_search):
        mock_search.return_value = self.mock_movie_data
        
        # First call, should fetch from TMDb and cache
        response = self.client.get(self.search_url, {'q': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if data is cached
        cached_data = cache.get('movie_search_test_1')
        self.assertIsNotNone(cached_data)
        self.assertEqual(len(cached_data['results']), 1)
        self.assertEqual(cached_data['results'][0]['title'], 'Test Movie')
        
        # Second call, should hit cache
        response = self.client.get(self.search_url, {'q': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Test Movie')
