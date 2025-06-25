"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Tests models."""

    def test_create_user_with_email_success(self):
        """Test create user with email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
  
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normolize(self):
        """Test email is normolized for new users."""
        sample_emails = [
            ['TEST1@EXAMPLE.com', 'TEST1@example.com'],
            ['test2@example.COM', 'test2@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='test1234',
            )
            self.assertEqual(user.email, expected)
