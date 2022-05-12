from enum import Enum


class ERRCODE(Enum):
    UNKNOWN = 0

    ITEM_NAME_MISSING = 1
    ATTACK_NAME_MISSING = 2
    ENEMY_NAME_MISSING = 3
    NODE_NAME_MISSING = 4
    ITEM_NAME_DUPLICATED = 5
    ATTACK_NAME_DUPLICATED = 6
    ENEMY_NAME_DUPLICATED = 7
    NODE_NAME_DUPLICATED = 8

    DIR_UNKNOWN = 10
    DIR_REPEATED_SYNONYM = 11
    DIR_REPEATED_DIRECTION = 12
    ATTACK_NEGATIVE_VALUE = 20
    ENEMY_STAT_SIZE = 30
    ENEMY_ATTACK_SIZE = 31
    ENEMY_IMAGE_MISSING = 32

    OBJECT_KEYS_DUPLICATED = 90
    OBJECT_KEY_MISSING = 91

class Error:
    errCode = ERRCODE.UNKNOWN
    file = "somefile"
    message = "you made an oopsie"

    def __init__(self, code, file, message):
        self.errCode = code
        self.file = file
        self.message = message
