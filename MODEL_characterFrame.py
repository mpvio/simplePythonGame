import tkinter as tk
from character import Character
from actions import Actions
from interactions import Interactions
from states import States

class CharacterFrame(tk.Frame):

    def __init__(self, master: tk.Tk, character: Character, allCharacters: list[Character] = None):
        super(CharacterFrame, self).__init__()
        self.character = character
        self.allChars = allCharacters
        self.master = master
        self.relief = tk.RAISED
        self.borderwidth = 5
        self.characterLength = 250
        self.labelLength = 35 #35
        self.stringVar = tk.StringVar()

        self.grid(
            row=self.character.team, #team 1,2 -> row 1,2
            column=self.character.id-1, #position 1,2,3 -> column 0,1,2
            sticky="nesw"
        )
        
        self.nameLabel = tk.Label(
            master=self,
            text=f"{self.character.getName():^{self.labelLength}}",
            wraplength=self.characterLength,
            anchor="center",
            justify="center"
        )
        self.nameLabel.grid(column=0, row=0, columnspan=3)

        self.atkHpLabel = tk.Label(
            master=self,
            wraplength=self.characterLength,
            anchor="center",
            justify="center"
        )
        self.atkHpLabel.grid(column=0, row=1, columnspan=3)

        self.actionLabel = tk.Label(
            master=self,
            wraplength=self.characterLength,
            anchor="center",
            justify="center"
        )
        self.actionLabel.grid(column=0, row=2, columnspan=3)

        self.targetLabel = tk.Label(
            master=self,
            wraplength=self.characterLength,
            anchor="center",
            justify="center"
        )
        self.targetLabel.grid(column=0, row=3, columnspan=3)

        self.stateLabel = tk.Label(
            master=self,
            wraplength=self.characterLength,
            anchor="center",
            justify="center"
        )
        self.stateLabel.grid(column=0, row=4, columnspan=3)

        #alivePlayer = self.character.team == 1 and self.character.isAlive()

        self.guardBtn = tk.Button(
            master=self,
            text="Guard",
            command=lambda: self.setAction(Actions.Guard)
        )
        self.guardBtn.grid(column=0, row=5)

        self.attackBtn = tk.Button(
            master=self,
            text="Attack",
            command=lambda: self.setAction(Actions.Attack)
        )
        self.attackBtn.grid(column=1, row=5)

        self.supportBtn = tk.Button(
            master=self,
            text="Support",
            command=lambda: self.setAction(Actions.Support)
        )
        self.supportBtn.grid(column=2, row=5)

        self.optionMenu = self.setTargetList() #row=6, columnspan=2
        self.optionMenu.grid_forget()

        self.confirmButton = tk.Button(
            master=self,
            text="Confirm",
            command= lambda: self.submitAction()
        )
        #self.confirmButton.grid(column=2, row=6, columnspan=1)
        self.confirmButton.grid_forget()

        self.comparisonsLabel = tk.Label(
            master=self,
            wraplength=self.characterLength,
            anchor="center",
            justify="center"
        )
        self.comparisonsLabel.grid(column=0, row=7, columnspan=3)

        self.updateAction()
        self.displayState()
        self.updateAll()

    def setTargetList(self):
        possibleTargets = []
        for c in self.allChars:
            if c.getName() == self.character.getName(): 
                continue
            elif c.isAlive() == False: 
                continue
            else: 
                possibleTargets.append(c.getRawName())
        
        if possibleTargets == []:
            self.stringVar.set("0 0")
        else:
            self.stringVar.set(possibleTargets[0])
        menu = tk.OptionMenu(self, self.stringVar, *possibleTargets)
        return menu

    def updateAll(self):
        self.updateHp()
        self.updateComparisons()
        self.updateButtons()
        self.displayAction()
        self.displayState()
        self.displayTarget()

    def updateHp(self):
        #f"{self.character.getName():^{self.labelLength}}"
        atkHp = f"ATK: {self.character.atk}, HP: {self.character.hp}"
        self.atkHpLabel["text"] =  f"{atkHp:^{self.labelLength}}"

    def updateAction(self):
        self.displayAction()
        if self.character.action in [Actions.Attack, Actions.Support]:
            self.optionMenu.grid(column=0, row=6, columnspan=2)
        else:
            self.optionMenu.grid_forget()
        self.confirmButton.grid(column=2, row=6, columnspan=1)

    def displayAction(self):
        #actionString = f"Action: {self.character.action.name}"
        self.actionLabel["text"] = f"{self.character.action.name:^{self.labelLength}}"

    def displayState(self):
        #stateString = f"State: {self.character.state.name}"
        self.stateLabel["text"] = f"{self.character.state.name:^{self.labelLength}}"

    def displayTarget(self):
        target = self.character.target
        if target == None: targetName = "No Target"
        elif type(target) == Character: targetName = target.getName()
        else: targetName = "NA"
        #targetString = f"Target: {targetName}"
        self.targetLabel["text"] = f"{targetName:^{self.labelLength}}"

    def updateComparisons(self):
        allComparisons = "\n".join([f"{comparison:^{self.labelLength}}" for comparison in self.character.get_table()])
        self.comparisonsLabel["text"] = allComparisons

    def updateButtons(self):
        if self.character.isAlive() == False or self.character.team == 2:
            self.guardBtn.grid_forget()
            self.supportBtn.grid_forget()
            self.attackBtn.grid_forget()
        else:
            self.optionMenu = self.setTargetList()
        self.confirmButton.grid_forget()
        self.optionMenu.grid_forget()
        # alive = self.character.isAlive()
        # if alive:
        #     if self.character.team == 2:
        #         self.guardBtn["text"] = ''.rjust(5, '🤖')
        #         self.supportBtn["text"] = ''.rjust(7, '🤖')
        #         self.attackBtn["text"] = ''.rjust(6, '🤖')    
        # else:
        #     self.guardBtn["text"] = ''.rjust(5, '💀')
        #     self.supportBtn["text"] = ''.rjust(7, '💀')
        #     self.attackBtn["text"] = ''.rjust(6, '💀')

    def reduceHp(self, hpChange: int):
        self.character.reduceHp(hpChange)
        self.updateHp()
        #self.atkHpLabel["text"] = f"ATK: {self.character.atk}, HP: {self.character.hp}"

    def setAction(self, action: Actions):
        self.character.setAction(action)
        self.updateAction()
        #self.actionLabel["text"] = f"{self.character.action.name}"

    def setState(self, state: States):
        self.character.state = state
        self.displayState()
        #self.stateLabel["text"] = f"{self.character.state.name}"

    def addComparison(self, character: Character, interaction: Interactions):
        self.character.addComparison(character, interaction)
        self.updateComparisons()

        #allComparisons = "\n".join(self.character.get_table())
        #self.comparisonsLabel["text"] = allComparisons

    def submitAction(self):
        #e.g. "1 1"
        if self.character.action == Actions.Guard:
            self.character.target = None
        else:
            targetTuple = tuple(map(int, self.stringVar.get().split(" ")))
            print(targetTuple, type(targetTuple))
            self.character.setTarget(self.getCharacter(targetTuple))
        self.confirmButton.grid_forget()
        self.optionMenu.grid_forget()
        self.displayTarget()
    
    def updateCharacters(self, characters: list[Character]):
        self.allChars = characters
        self.optionMenu.grid_forget()

    def getCharacter(self, targetTuple: tuple[int, int]):
        for ch in self.allChars:
            if ch.team == targetTuple[0] and ch.id == targetTuple[1]: 
                print("Found", ch.getName())
                return ch
        print("Going with None")
        return None