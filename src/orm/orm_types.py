from abc import ABC, abstractmethod

import datetime as dt
from PIL import Image as PILImage

from . import logging_config
import logging

logger = logging.getLogger(__name__)

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


class Image(OrmTypeBase):
    file_name: str = None
    image: PILImage = None

    def __init__(self, file_name: str):
        self.file_name = file_name

    def __str__(self) -> str:
        return self.file_name

    def __enter__(self) -> PILImage:
        self.image = PILImage.open(self.file_name)
        return self.image
    
    def __exit__(self, exc_type, exc_value, tb) -> True:
        self.image.close()
        logger.debug(f"Image '{settings.IMAGES_PATH / self.file_name}' is closed")

        if exc_type is not None:
            logger.warning(f"Exception with image occured: {exc_value}")
        return exc_type is None
