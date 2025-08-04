from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "password2": "testpass123",
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_user_registration_password_mismatch(self):
        self.user_data["password2"] = "wrongpassword"
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="testuser").exists())


class UserProfileTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.profile_url = reverse("user-profile")

        # Get JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_get_user_profile_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "test@example.com")

    def test_get_user_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        update_data = {"email": "newemail@example.com"}
        response = self.client.patch(self.profile_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")
