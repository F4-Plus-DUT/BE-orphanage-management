from enum import Enum, IntEnum


class StringEnum(str, Enum):
    """Like IntEnum, it supports for string values"""


class Flag(IntEnum):
    ON = 1
    OFF = 0
