from enum import Enum
class ERRCODE(Enum):
    UNKNOWN = 0
    DIR_UNKNOWN = 10
    DIR_REPEATED_SYNONYM = 11

class Error:
    errCode = ERRCODE.UNKNOWN
    file = "somefile"
    message = "you made an oopsie"

    def __init__(self, code, file, message):
        self.errCode = code
        self.file = file
        self.message = message
