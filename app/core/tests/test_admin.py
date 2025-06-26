"""
Test for django admin modifications
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Tests for django admin."""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_super_user(
            email='admin@example.com',
            password='test123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@exampl.com',
            password='testpass23',
            name='TestName',
        )
        