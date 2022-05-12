from enum import Enum


class ERRCODE(Enum):
    UNKNOWN = 0
    DIR_UNKNOWN = 10
    DIR_REPEATED_SYNONYM = 11
    DIR_REPEATED_DIRECTION = 12
    ATTACK_NEGATIVE_VALUE = 20
    ENEMY_STAT_SIZE = 30
    ENEMY_ATTACK_SIZE = 31
    ENEMY_IMAGE_MISSING = 32
    ITEM_NAME_DUPLICATED = 13
    ATTACK_NAME_DUPLICATED = 14
    ENEMY_NAME_DUPLICATED = 15
    NODE_NAME_DUPLICATED = 16
    NODE_DOES_NOT_EXISTS = 17
    NODE_EVENT_DOES_NOT_EXIST = 17
    EVENT_MISSING_FIELD = 18
    ENEMY_DOES_NOT_EXIST = 19

    OBJECT_KEYS_DUPLICATED = 90

class Error:
    errCode = ERRCODE.UNKNOWN
    file = "somefile"
    message = "you made an oopsie"

    def __init__(self, code, file, message):
        self.errCode = code
        self.file = file
        self.message = message
