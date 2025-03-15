from enum import Enum

class Interactions(Enum):
    Neutral = 0
    SelfIsGenerative = 1
    SelfIsDestructive = 2
    OtherIsGenerative = -1
    OtherIsDestructive = -2