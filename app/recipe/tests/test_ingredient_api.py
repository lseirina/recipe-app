""""Tests for ingredient API"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Ingredient,
    Recipe
    )
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    """Return detail_utl"""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_user(email='test@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicIngredientApiTest(TestCase):
    """Test for unauthorized user."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test requireing auth for retrieving ingredient"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """Tests for authorized user"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingrediernts(self):
        """Test retrieving ingredients successfull."""
        Ingredient.objects.create(user=self.user, name='Banana')
        Ingredient.objects.create(user=self.user, name='Flour')

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """Test ingredient limited to authenticated user"""
        user2 = create_user(email='user2@example.com', password='pass345')
        Ingredient.objects.create(user=user2, name='Potato')
        ingredient = Ingredient.objects.create(user=self.user, name='Bread')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_upgrade_ingredient(self):
        """Test updating ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='Egg')
        payload = {'name': 'Flour'}
        url = detail_url(ingredient.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_clear_ingredient(self):
        """"Test clearing the ingredient"""
        ingredient = Ingredient.objects.create(user=self.user, name='Ice')
        url = detail_url(ingredient.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())

    def test_filter_ingredient_by_assign_recipe(self):
        """Test filtering ingredients by those assinged to recipe."""
        ing1 = Ingredient.objects.create(user=self.user, name='Apples')
        ing2 = Ingredient.objects.create(user=self.user, name='Turkey')
        recipe = Recipe.objects.create(
            user=self.user,
            title='Apples Crumble',
            time_minutes=20,
            price=Decimal('3.49')
        )
        recipe.ingredients.add(ing1)
        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})
        s1 = IngredientSerializer(ing1)
        s2 = IngredientSerializer(ing2)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filter_ingredient_unique(self):
        """Test filtering return unique ingredient assign to a few recipes."""
        ing = Ingredient.objects.create(user=self.user, name='Egg')
        Ingredient.objects.create(user=self.user, name='Milk')
        r1 = Recipe.objects.create(
            user=self.user,
            title='Eggs Beendict',
            time_minutes=30,
            price=Decimal('45.50')
        )
        r2 = Recipe.objects.create(
            user=self.user,
            title='Herb Egg',
            time_minutes=40,
            price=Decimal('30.40')
        )
        r1.ingredients.add(ing)
        r2.ingredients.add(ing)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
