from elements import Elements
from actions import Actions
from states import States
from interactions import Interactions
#from character import Character

class Character:
    team: int
    id: int
    hp: int
    atk: int
    element: Elements
    state: States
    action: Actions
    target: any #tuple[int, int] #target: (team, id)
    comparisons: set[tuple[any, Interactions]] 
    #comparisons: [(Character, interaction)]

    def __init__(self, team, id, element):
        self.team = team
        self.id = id
        self.hp = 20
        self.atk = 4
        self.element = element
        self.state = States.Default
        self.action = Actions.Idle
        self.target = None
        self.comparisons = set()

    def __str__(self):
        return f"{self.team}|{self.id} {self.hp}|{self.atk}"
    
    def getName(self):
        #return f"T {self.team}|ID {self.id}"
        return f"Team {self.team}|Pos. {self.id}"
    
    def getRawName(self):
        return f"{self.team} {self.id}"
    
    def isAlive(self):
        return self.hp > 0
    
    def getHp(self):
        return self.hp
    
    def reduceHp(self, value: int):
        if self.action == Actions.Guard:
            value = value/2
        self.hp = (int) (self.hp - value)

    def changeState(self, state: States):
        self.state = state

    def getAction(self):
        return self.action
    
    def setAction(self, action: Actions):
        self.action = action

    def getTarget(self):
        return self.target

    def setTarget(self, team: int, id: int):
        self.target = (team, id)
    
    def setTarget(self, targetTuple: tuple[int, int]):
        self.target = targetTuple

    def setTarget(self, target: any):
        self.target = target

    def addComparison(self, other, interaction: Interactions):
        self.comparisons.add((other, interaction))
    
    def getComparison(self, other):
        for chara, interact in self.comparisons:
            if chara == other: return interact
        return None
    
    #debug functions
    def combatInfo(self):
        return f"{self.state}|{self.action} {self.target}"
    
    def get_element(self):
        return self.element.name
    
    def getAll(self):
        return f"{self} {self.combatInfo()} {self.get_element()}"

    def get_table(self):
        charInterTable = list()
        for (character, interaction) in self.comparisons:
            charInterTable.append(f"{self.getName()} -> {character.getName()} = {interaction}")
        return charInterTable
