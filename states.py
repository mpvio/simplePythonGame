from enum import Enum

class States(Enum):
    Default = 0
    Buffed = 2
    SuperBuffed = 4
    Debuffed = -2
    SuperDebuffed = -4