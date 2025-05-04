import unittest

class test_tests(unittest.TestCase):
    def test_sum(self):
        x = 1
        y = 3
        self.assertEqual(x+y, 4)

    def test_div(self):
        x = 1
        y = 0
        with self.assertRaises(ZeroDivisionError):
            return x/y
