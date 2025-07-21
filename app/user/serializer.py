"""
Serializer for user API view.
"""
from django.contrib.auth import (get_user_model, authenticate)

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user model."""
    class Meta:
        model = get_user_model()
        fields = ['password', 'email', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)
    

class TokenSerializer(serializers.Serializer):
    """Serializer for token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        'style_not'='password'
        )
    
    def validate(self, attrs):
        """Validate probided credentials"""
        email = self.get(attrs, email)
        password = self.get(attrs, password)
        
        user = validate(
            request=self.context.get('request'),
            name=email,
            password=password,
        )
        
        if not user:
            msg = "Not available eith provided credentials"
            raise serializers.ValidationError(msg, code=authorization)
        
        attrs['user'] = user
        return attrs
        
