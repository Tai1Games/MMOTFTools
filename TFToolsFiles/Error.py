from enum import Enum


class ERRCODE(Enum):
    UNKNOWN = 0

    NAME_ITEM_MISSING = 1
    NAME_ATTACK_MISSING = 2
    NAME_ENEMY_MISSING = 3
    NAME_NODE_MISSING = 4
    NAME_ITEM_DUPLICATED = 5
    NAME_ATTACK_DUPLICATED = 6
    NAME_ENEMY_DUPLICATED = 7
    NAME_NODE_DUPLICATED = 8

    DIR_UNKNOWN = 10
    DIR_REPEATED_SYNONYM = 11
    DIR_REPEATED_DIRECTION = 12

    ATTACK_NEGATIVE_VALUE = 20
    ATTACK_MISSING_REFERENCES = 21

    ENEMY_STAT_SIZE = 30
    ENEMY_ATTACK_SIZE = 31
    ENEMY_IMAGE_MISSING = 32
    ENEMY_JSON_REFERENCE = 33
    
    NODE_DOES_NOT_EXISTS = 40
    NODE_EVENT_DOES_NOT_EXIST = 41
    EVENT_MISSING_FIELD = 42
    MAP_ENEMY_DOES_NOT_EXIST = 43
    MAP_ITEM_DOES_NOT_EXIST = 44

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
