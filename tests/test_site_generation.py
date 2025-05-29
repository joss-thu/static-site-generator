import unittest
from src.site_operations import (
    extract_title
)
    
# ------------------------------------------------------------------------
# Test Title extraction
# ------------------------------------------------------------------------
# positive case
class Test_Site_Generation(unittest.TestCase):
    def test_extract_heading(self):
        markdown = '''
# Main Heading

contents with paragraph here
'''
        self.assertEqual(extract_title(markdown), 'Main Heading')

# Negative case
    def test_extract_heading_neagative(self):
        markdown = '''
## Main Heading

contents with paragraph here
'''
        with self.assertRaises(ValueError):
            extract_title(markdown)
