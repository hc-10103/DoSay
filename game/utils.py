from .board import Board

def print_board(board: Board):
    for line in board.board:
        print(*(f"{v:1d}" for v in line))