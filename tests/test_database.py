import unittest
import logging

logging.disable()

import os

from . import settings
from src import database

def get_serializable_format(columns, values):
    braces_str = '({})'
    str_builder_1 = []
    str_builder_2 = []
    for k, v in zip(columns, values):
        if v is not None:
            str_builder_1.append(k)
            str_builder_2.append(f"'{v}'")
    return (
        braces_str.format(', '.join(str_builder_1)),
        braces_str.format(', '.join(str_builder_2))
        )


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()

    def test_singleton(self):
        self.assertEqual(id(self.database), id(database.Database()))

    def test_table_creating(self):
        db = self.database
        try:
            db._create_database('temp.db')
        except Exception as e:
            self.fail(e)
        finally:
            db.close()
            os.remove('temp.db')

    def test_insert_read_and_delete_from_table(self):
        db = self.database
        db._create_database('temp.db')

        try:
            users_right_data = (
                ('users', (('tg_user_id',), (1,))),
                ('users', (('tg_user_id', 'state'), (12, 3))),
                ('users', (('tg_user_id', 'additional_info'), (123, 'batman')))
            )
            wrong_data = (
                ('users', (('unexisting_column',), ('asdasd',))),
                ('not_users', (('name',), ('asdasd',))),
            )

            for table, data in users_right_data:
                try:
                    db._insert_in_table(table, get_serializable_format(data[0], data[1]))
                except Exception as e:
                    self.fail(e)

            for table, data in wrong_data:
                try:
                    db._insert_in_table(table, get_serializable_format(data[0], data[1]))
                    self.fail()
                except Exception as e:
                    pass
            
            for id, (table, data) in enumerate(users_right_data):
                id += 1
                try:
                    from_table_data = db._get_table_data_by_column('users', 'id', id)
                    for col in data[1]:
                        self.assertIn(col, from_table_data)

                except Exception as e:
                    self.fail(e)

            for id in range(1, len(users_right_data) + 1):
                try:
                    correct = db._get_table_data_by_column('users', 'id', id) is not None
                    db._delete_table_data_by_column('users', 'id', id)
                    correct = correct and db._get_table_data_by_column('users', 'id', id) is None

                    self.assertTrue(correct)

                except Exception as e:
                    self.fail(e)
        finally:
            db.close()
            os.remove('temp.db')

if __name__ == "__main__":
    unittest.main()
