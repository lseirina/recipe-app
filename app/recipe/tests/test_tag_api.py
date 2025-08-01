"""Test for the tag API."""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Tag,
    Recipe
    )
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


def detail_url(tag_id):
    """Create and return detail url for tag."""
    return reverse('recipe:tag-detail', args=[tag_id])


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
        res = self.client.get(TAGS_URL)

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
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tag_limited_to_user(self):
        """Test tag is limited to authenticated user."""
        user2 = create_user(email='user2@ec=xample.com', password='pass123')
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Desert')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """Test partial updating tag."""
        tag = Tag.objects.create(user=self.user, name='After Dinner')
        payload = {'name': 'Dessert'}
        url = detail_url(tag.id)

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """"Test deleting tag."""
        tag = Tag.objects.create(user=self.user, name='Vegan')
        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())

    def test_filter_tags_by_assigned_recipe(self):
        """Test filtering tags by those assigned to recipe."""
        tag1 = Tag.objects.create(user=self.user, name='Dessert')
        tag2 = Tag.objects.create(user=self.user, name='Vegan')
        r1 = Recipe.objects.create(
            user=self.user,
            title='Pie',
            time_minutes=39,
            price=Decimal('45.56')
        )

        r1.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})
        s1 = TagSerializer(tag1)
        s2 = TagSerializer(tag2)

        self.assertequal(res.status_code, status.HTTP_200_OK)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data. res.data)
