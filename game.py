from board import Minesweeper
from global_functions import movement_menu

game = Minesweeper()  # add here (rows, columns) to change the size f the board.
game.play(movement_menu)
