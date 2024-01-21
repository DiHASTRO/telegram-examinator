from abc import ABC, abstractmethod

import datetime as dt

from .. import settings

class OrmTypeBase(ABC):
    @abstractmethod
    def __init__(self, from_str: str):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class DateTime(OrmTypeBase):
    date_time: dt.datetime = None

    def __init__(self, from_str: str):
        self.date_time = dt.datetime.strptime(from_str, settings.DATE_TIME_FORMAT)
    
    def __str__(self) -> str:
        return self.date_time.strftime(settings.DATE_TIME_FORMAT)
