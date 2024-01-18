from abc import ABC, abstractmethod

from . import database

class ModelBase(object):
    def __str__(self):
        to_join = []
        for k, v in self.__dict__.items():
            to_join.append(f'{k}={v}')
        return f"{self.__class__.__name__}[{', '.join(to_join)}]"

    def get_serializable_format(self):
        braces_str = '({})'
        str_builder_1 = []
        str_builder_2 = []
        for k, v in self.__dict__.items():
            if v is not None:
                str_builder_1.append(k)
                str_builder_2.append(str(v))
        return (
            braces_str.format(', '.join(str_builder_1)),
            braces_str.format(', '.join(str_builder_2))
            )


class User(ModelBase):
    id: int = None
    tg_user_id: int = None
    state: int = None
    additional_info: int = None

    @staticmethod
    def get_user_by_id(id: int):
        return User(database.Database()._get_user_data_by_column('id', id))

    @staticmethod
    def get_user_by_tg_user_id(tg_user_id: int):
        data_from_database = database.Database()._get_user_data_by_column('twwg_user_id', tg_user_id)
        new_user = User(*data_from_database[1:])
        new_user.id = data_from_database[0]
        
        return new_user

    def __init__(self, tg_user_id: int, state: int = None, additional_info: int = None):
        self.tg_user_id = tg_user_id
        self.state = state
        self.additional_info = additional_info

    def save(self):
        database.Database()._insert_user(self.get_serializable_format())        
