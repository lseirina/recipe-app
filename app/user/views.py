"""
Views for User Api.
"""
from rest_framework import (
    generics,
    authentication,
    permissions,
    )
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializer import (UserSerializer, AuthTokenSerializer)


class CreateUserView(generics.CreateAPIView):
    """Create new user in the system."""
    serializer_class = UserSerializer
    
    
class CreateTokenView(ObtainAuthToken):
    """Create token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    

class ManageView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user."""
        return self.request.user
