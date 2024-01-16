from abc import ABC, abstractmethod

from . import database

class ModelBase(ABC):
    
    @abstractmethod
    def __iter__(self):
        pass


class User(ModelBase):
    id: int = None
    tg_user_id: int = None
    state: int = None
    additional_info: int = None

    def __init__(self, tg_user_id: int, state: int = 0, additional_info: int = None):
        self.tg_user_id = tg_user_id
        self.state = state
        self.additional_info = additional_info

    def __iter__(self):
        for field in (self.id, self.tg_user_id, self.state, self.additional_info):
            yield field

    def save(self):
        database.Database()._insert_user(tuple(self))        
