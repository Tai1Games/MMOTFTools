from enum import Enum


class ERRCODE(Enum):
    UNKNOWN = 0
    NAME_ITEM_DUPLICATED = 1   
    NAME_ENEMY_DUPLICATED = 2
    NAME_NODE_DUPLICATED = 3
    NAME_ATTACK_DUPLICATED = 4

    DIR_UNKNOWN = 10
    DIR_REPEATED_SYNONYM = 11
    DIR_REPEATED_DIRECTION = 12

    ATTACK_NEGATIVE_VALUE = 20

    ENEMY_STAT_SIZE = 30
    ENEMY_ATTACK_SIZE = 31
    ENEMY_IMAGE_MISSING = 32
    ENEMY_JSON_REFERENCE = 33
    
    NODE_DOES_NOT_EXISTS = 40
    NODE_EVENT_DOES_NOT_EXIST = 41
    EVENT_MISSING_FIELD = 42
    MAP_ENEMY_DOES_NOT_EXIST = 43
    MAP_ITEM_DOES_NOT_EXIST = 44

    ITEM_ITEM_DOES_NOT_EXIST = 50
    ITEM_ATTACK_DOES_NOT_EXIST = 51
    ITEM_IMAGE_DOES_NOT_EXIST = 52
    ITEM_ENEMY_DOES_NOT_EXIST = 53
    ITEM_AUDIO_DOES_NOT_EXIST = 54

    OBJECT_KEYS_DUPLICATED = 90
    ATACK_MISSING_REFERENCES = 25

class Error:
    errCode = ERRCODE.UNKNOWN
    file = "somefile"
    message = "you made an oopsie"

    def __init__(self, code, file, message):
        self.errCode = code
        self.file = file
        self.message = message
