from enum import Enum
class ERRCODE(Enum):
    UNKNOWN = 0
    DIR_UNKNOWN = 10
    DIR_REPEATED_SYNONYM = 11
    DIR_REPEATED_DIRECTION = 12
    ITEM_NAME_DUPLICATED = 13
    ATTACK_NAME_DUPLICATED = 14
    ENEMY_NAME_DUPLICATED = 15
    NODE_NAME_DUPLICATED = 16
    NODE_DOES_NOT_EXISTS = 17

class Error:
    errCode = ERRCODE.UNKNOWN
    file = "somefile"
    message = "you made an oopsie"

    def __init__(self, code, file, message):
        self.errCode = code
        self.file = file
        self.message = message
