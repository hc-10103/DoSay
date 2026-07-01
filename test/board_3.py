import os, sys, random
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game import Board, utils

board = Board(board_size=(30, 40))

while True:
    valid_actions = board.get_valid_actions()
    if len(valid_actions) > 0:
        action = random.choice(valid_actions)
        board.do_action(action)
    else:
        utils.print_board(board)
        break

print("GAME OVER!")
print(f"LEFT APPLE: {np.count_nonzero(board.board != 0)}")