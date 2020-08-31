import glob
import logging
import logging.config
import os
from logging import NullHandler

logging.config.fileConfig(os.getenv("LOG_CONF_PATH"))
logging.getLogger(__name__).addHandler(NullHandler())

__all__ = [
    os.path.split(os.path.splitext(file)[0])[1]
    for file in glob.glob(os.path.join(os.path.dirname(__file__), "[a-zA-Z0-9]*.py"))
]
