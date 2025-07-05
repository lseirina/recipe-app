"""
Tests for user api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.url import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_API = reverse('user:create')


def create_user(**params):
    """Create and return user."""
    return get_user_model().objects.create(**params)

