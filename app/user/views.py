"""
Views for User Api.
"""
from rest_framework import generics

from user.serializer import UserSerializer


class UserView(generics.CreateView):
    """Create view for user object."""
    serializer = UserSerializer
