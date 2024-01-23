from games.PirateMaker.code import main as Pirate
from games.PydewValley.code import main as Pydew
from games.SpaceInvaders.code import main as Invaders
from games.Zelda.code import main as Zel

from games.SopaLetras import main as Letter

def exec_game(game_name):
    func = globals()[game_name]
    func()

def SopaLetras(data = None):
    Letter.run_game(data)

def PirateMaker():
    Pirate.run_game()
    
def PydewValley():
    Pydew.run_game()

def SpaceInvaders():
    Invaders.run_game()

def Zelda():
    Zel.run_game()