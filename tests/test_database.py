import unittest
import logging

import os

from . import settings
from src import database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database1 = database.Database()
        self.database2 = database.Database()

    def test_singleton(self):
        self.assertEqual(id(self.database1), id(self.database2))

    def test_table_creating(self):
        # log = logging.getLogger("TestDatabase.test_table_creating")
        db = self.database1
        try:
            db._create_database('temp.db')
        except Exception as e:
            # log.debug(e)
            self.fail(e)
        finally:
            db.close()
            os.remove('temp.db')


if __name__ == "__main__":
    unittest.main()
