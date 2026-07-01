import numpy as np
from numpy.typing import NDArray
from dataclasses import dataclass

def compute_prefix(board: NDArray) -> NDArray:
    height, width = board.shape
    prefix = np.zeros((height + 1, width + 1), dtype=np.int64)
    for i in range(height):
        for j in range(width):
            prefix[i+1][j+1] = (
                board[i][j] +
                prefix[i][j+1] +
                prefix[i+1][j] -
                prefix[i][j]
            )

    return prefix


@dataclass 
class FeatureContext:
    board: NDArray[np.int8] # 숫자 배열의 좌푯값
    prefix: NDArray  # 누적합
    count_by_value: dict[int, int]      #숫자별 남아있는 개수

    @classmethod
    def from_board(cls, board: NDArray) -> "FeatureContext":
        prefix = compute_prefix(board)
        counts = {v: int((board == v).sum()) for v in range(1, 10)}
        return cls(board=board, prefix = prefix, count_by_value = counts)
    

    
    

    