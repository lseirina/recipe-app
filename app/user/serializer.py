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

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None) 
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}
        )

    def validate(self, attrs):
        """Validate and authenticate user."""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = "Unabale to authrnticate with provided credentials"
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
