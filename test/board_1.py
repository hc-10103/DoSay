import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game import Board, Action, utils

board = Board(board_size=(9, 18))

utils.print_board(board)

valid_actions = board.get_valid_actions()
print(valid_actions)

inp = input("r1 c1 r2 c2 : ")
r1, c1, r2, c2 = map(int, inp.split())
action = Action((r1, c1), (r2, c2))
board.do_action(action)

utils.print_board(board)