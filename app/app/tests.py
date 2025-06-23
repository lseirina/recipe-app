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
        
    def test_subtract_numbers(self):
        """Test subtracting numbers"""
        res = calc.subtract(10, 15)
        
        self.assertEqual(res, 5)