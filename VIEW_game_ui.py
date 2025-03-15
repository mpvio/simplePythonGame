import tkinter as tk
from character import Character
from MODEL_characterFrame import CharacterFrame as cf
from elements import Elements
from game_master import GameMaster
from MODEL_gameWindow import GameWindow as gw

#global params
wraplength = 750
characterLength = (int) (wraplength/3)

def start_up():
    gm = GameMaster()
    window = gw(gm)

    window.mainloop()
    # window = tk.Tk()
    # window.title("GAME")
    # window.columnconfigure(0, weight=1, minsize=20)
    # window.columnconfigure(1, weight=1, minsize=20)
    # window.columnconfigure(2, weight=1, minsize=20)
    # window.rowconfigure(0, weight=1, minsize=20)
    # window.rowconfigure(1, weight=1, minsize=20)

    # gm = GameMaster()
    # for ch in gm.allCharacters:
    #     cf(window, ch, gm.allCharacters[:])

    # window.mainloop()



if __name__ == "__main__":
    start_up()