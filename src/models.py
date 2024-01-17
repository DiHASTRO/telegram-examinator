from abc import ABC, abstractmethod

from . import database

class ModelBase(object):
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

    def __init__(self, tg_user_id: int, state: int = None, additional_info: int = None):
        self.tg_user_id = tg_user_id
        self.state = state
        self.additional_info = additional_info

    def save(self):
        print(self.get_serializable_format())
        database.Database()._insert_user(self.get_serializable_format())        


