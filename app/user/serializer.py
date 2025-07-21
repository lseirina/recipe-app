"""
Serializer for user API view.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model."""
    class Meta:
        model = get_user_model()
        fields = ['name', 'password', 'email']
        extra_fields = [{'passwords': {'writen_inly': True, 'min_length': 5}}]
        
    def create(self, **validation_data):
        """Create and return user with validated data"""
        return get_user_model.objects.create(**validation_data)