import numpy as np
from numpy.typing import NDArray
from action import Action

class Board():
    def __init__(self):
        self.size = (10, 17)
        self.board = self._generate_board()

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

    def _generate_board(self) -> NDArray[np.int8]:  # 17x10
        _board = np.random.randint(1, 10, size=self.size, dtype=np.int8)
        return _board