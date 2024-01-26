import logging.config

BASE_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "string": {
            "format": "%(levelname)s [%(asctime)s] %(module)s: %(message)s ",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "string",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "string",
            "filename": "app.log",
            "maxBytes": 65536,
            "backupCount": 2,
        }
    },
    "loggers": {"": {"handlers": ["stdout", "file"], "level": "DEBUG"}},
}

logging.config.dictConfig(BASE_LOGGING)
