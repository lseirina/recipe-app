"""
Sample tests
"""
from django.test import SimpleTestCase

from app import calc

class CalcTest(SimpleTestCase):
    """Test the calc module"""
    
    def test_add_number(self):
        """Test addition numbers together"""
        res = calc.add(5, 3)
        
        self.assertEqual(res, 8)