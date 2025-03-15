import tkinter as tk
from game_master import GameMaster
from MODEL_characterFrame import CharacterFrame as cf

class GameWindow(tk.Tk):
    def __init__(self, gm: GameMaster):
        super(GameWindow, self).__init__()
        self.gm = gm
        #self.charFrames = list[cf]

        self.title("GAME")
        self.columnconfigure(0, weight=1, minsize=20)
        self.columnconfigure(1, weight=1, minsize=20)
        self.columnconfigure(2, weight=1, minsize=20)
        self.rowconfigure(0, weight=1, minsize=20)
        self.rowconfigure(1, weight=1, minsize=20)
        self.rowconfigure(2, weight=1, minsize=20)

        self.populateFrames()
        # self.frameList = []
        # for ch in gm.allCharacters:
        #     newFrame = cf(self, ch, gm.allCharacters[:])
        #     self.frameList.append(newFrame)
        
        self.startTurn = tk.Button(
            master=self,
            text="FINALISE",
            command= lambda: self.finalisePlayerActions()
        )

        self.startTurn.grid(row=0, column=0, columnspan=2)

        self.restart = tk.Button(
            master=self,
            text="RESTART",
            command = lambda: self.restartGame()
        )

        self.restart.grid_forget()

    def finalisePlayerActions(self):
        self.gm.setAIActions()
        self.gm.executeTeamActions()
        for frame in self.frameList:
            #todo: finalize only works if all three player characters have options made?
            frame.updateAll()
            frame.updateCharacters(self.gm.allCharacters)
        if self.gm.gameOver():
            self.restart.grid(row=0, column=2, columnspan=1)
    
    def restartGame(self):
        self.gm = GameMaster()
        self.populateFrames()
        self.restart.grid_forget()

    def populateFrames(self):
        self.frameList = []
        for ch in self.gm.allCharacters:
            newFrame = cf(self, ch, self.gm.allCharacters[:])
            self.frameList.append(newFrame)