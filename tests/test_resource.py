import unittest
from models.resource import Resource

class TestResource(unittest.TestCase):
    def test_create_user(self):
        # Test creating a new user
        r = Resource("R")
        self.assertEqual(r.name, "R")
        self.assertEqual(r.price, 10)

if __name__ == '__main__':
    unittest.main()