"""Test for the tag API."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


def create_user(email='test@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


class PublicTagsApiTests(TestCase):
    """Tests for unauthorized user."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth required for retrieving tags."""
        res = self.client(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
class PrivateTagsTests(TestCase):
    """Tests for authenticated requests."""
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
    def test_retrieve_tags(self):
        """Test retrieving tags successfull."""
        Tag.objects.create(
            user=self.user,
            name='Vegan'
        )
        Tag.objects.create(
            user=self.user,
            name='Desert'
        )
        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)