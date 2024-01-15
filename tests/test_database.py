import unittest
import settings

from src import database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database1 = database.Database()
        self.database2 = database.Database()

    def test_singleton(self):
        self.assertEqual(id(self.database1), id(self.database2))

if __name__ == "__main__":
    unittest.main()
