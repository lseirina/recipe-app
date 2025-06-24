"""
Django command to wait for db to be available.
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django management command to wait for database."""
    def handle(self, *args, **options):
        pass