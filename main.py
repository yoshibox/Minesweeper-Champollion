from fenetre import *
from logique import *

logic = logique(12)
board = Board(logic)


board.start() # Evenement bloquant

board.quit()