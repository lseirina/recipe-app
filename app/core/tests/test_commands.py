"""Tests django commands."""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalRrror
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_dn.Command.check')
class CommandTests(SimpleTestCase):
    """Tests commands."""
    def test_wait_for_db(self, patched_check):
        """Test comand when db is ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(database=['default'])
