import numpy as np
from numpy.typing import NDArray
from .action import Action

class Board():
    def __init__(self, init_board: NDArray[np.int8] | None = None, board_size: tuple[int, int] | None = None):
        if init_board is None and board_size is None:
            raise Exception("Both board_size and init_board cannot be None.")
        elif init_board is None:
            self.size = board_size # type: ignore
            self.board = _generate_board(self.size)
        elif board_size is None:
            self.size: tuple[int, int] = init_board.shape
            self.board = init_board
        else:
            if init_board.shape != board_size:
                raise Exception("board_size does not match init_board.size.")
            self.size = board_size
            self.board = init_board

    def do_action(self, action: Action) -> bool | NDArray[np.int8]:
        if not self.is_valid_action(action):
            return False
        
        self.get_area(action)[:] = 0
        return self.board


    def is_done(self) -> tuple[bool, bool]:
        actions = self.get_valid_actions()

        is_over = len(actions) == 0
        is_all_clear = self.board.sum() == 0

        return (is_over, is_all_clear)

    # 아 몰라 일단 구현해!!!!!!!!!
    def get_valid_actions(self) -> list[Action]:
        valid_actions = []
        for r1 in range(self.size[0]):
            for r2 in range(r1, self.size[0]):
                for c1 in range(self.size[1]):
                    for c2 in range(c1, self.size[1]):
                        action = Action((r1, c1), (r2, c2))
                        area = self.get_area(action)
                        area_sum = area.sum()

                        if area_sum == 10:
                            valid_actions.append(action)
                        elif area_sum > 10:
                            break

        return valid_actions

    def get_area(self, action: Action) -> NDArray[np.int8]:
        r1 = action.top_left[0]  # 시작 row
        c1 = action.top_left[1]  # 시작 column

        r2 = action.bottom_right[0]  # 시작 row
        c2 = action.bottom_right[1]  # 시작 column

        return self.board[r1:r2+1, c1:c2+1]
    
    def is_valid_action(self, action: Action) -> bool:
        area = self.get_area(action)
        action_valid = area.sum() == 10

        return action_valid
    
def _generate_board(size) -> NDArray[np.int8]:
    _board = np.random.randint(1, 10, size=size, dtype=np.int8)
    return _board