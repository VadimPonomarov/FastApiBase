import sys
from enum import Enum
from typing import Any, TextIO


class LoguruFormat(Enum):
    BASE: str = "<level>{level}: - {time:HH:mm:ss} - {file} - {function} - {line} - {message}</level>"


class LoguruSink(Enum):
    STD_OUT: TextIO | Any = sys.stdout
