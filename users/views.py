from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from .serializers import RegisterSerializer, UserSerializer

@extend_schema(
    tags=['Authentication'],
    description='Register a new user account. No authentication required.',
)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(
    tags=['Authentication'],
    description='Retrieve or update the authenticated user\'s profile. Requires authentication.',
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
