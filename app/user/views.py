"""
Views for User Api.
"""
from rest_framework import generics

from user.serializer import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create new user in the system."""
    serializer_class = UserSerializer
