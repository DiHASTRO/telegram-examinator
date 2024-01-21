from abc import ABC, abstractmethod
from typing import Any

from .. import database

class ModelBase(object):
    associated_table = None

    @classmethod
    def get_object_by(cls, column, value):
        data_from_database = database.Database()._get_table_data_by_column(cls.associated_table, column, value)
        new_object = cls.__new__(cls)
        new_object.__init__(*data_from_database[1:])
        new_object.id = data_from_database[0]

        return new_object

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
                str_builder_2.append(f"'{v}'")
        return (
            braces_str.format(', '.join(str_builder_1)),
            braces_str.format(', '.join(str_builder_2))
            )

    def save(self):
        database.Database()._insert_in_table(self.associated_table, self.get_serializable_format())


class User(ModelBase):
    associated_table = 'users'

    id: int = None
    tg_user_id: int = None
    state: int = None
    additional_info: int = None

    @classmethod
    def get_by_id(cls, id: int):
        return cls.get_object_by('id', id)

    @classmethod
    def get_by_tg_user_id(cls, tg_user_id: int):
        return cls.get_object_by('tg_user_id', tg_user_id)

    def __init__(self, tg_user_id: int, state: int = None, additional_info: int = None):
        self.tg_user_id = tg_user_id
        self.state = state
        self.additional_info = additional_info


class Subject(ModelBase):
    associated_table = 'subjects'

    id: int = None
    name: str = None
    owner_user_id: int = None
    __owner_user: User = None

    @classmethod
    def get_by_id(cls, id: int):
        return cls.get_object_by('id', id)

    @property
    def owner_user(self) -> User:
        if self.__owner_user is None:
            self.__owner_user = User.get_by_id(self.owner_user_id)
        return self.__owner_user

    def __init__(self, name: str = None, owner_user_id: int = None):
        self.name = name
        self.owner_user_id = owner_user_id


class Attempt(ModelBase):
    associated_table = 'attempts'
    
    date: str = None
    user_id: int = None
    subject_id: int = None
    grade: float = None