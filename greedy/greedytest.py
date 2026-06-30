import random
import numpy as np
from game import Board, Action
import copy

class GreedyAgent:
    """
    동작 방식:
      1. 시작점 후보들을 복합 점수(고립위험 + 높은숫자 + 가장자리)로 랭킹
      2. 점수 높은 시작점부터 시도
      3. 해당 시작점을 포함하는 합10 사각형 중 최적 액션 선택
      4. 후보 없으면 다음 순위 시작점으로 재시도
    """

    def __init__(self, max_retries: int = 30,
                 w_value: float = 1.0,
                 w_edge: float = 1.0,
                 w_isolation: float = 1.0):
        self.max_retries = max_retries
        # 시작점 선택용 가중치 (임의 설정 - 실험으로 튜닝 예정)
        self.w_value = w_value
        self.w_edge = w_edge
        self.w_isolation = w_isolation

    # ------------------------------------------------------------------ #
    #  퍼블릭 API
    # ------------------------------------------------------------------ #

    def select_action(self, board: Board) -> Action | None:
        rows, cols = board.size
        non_zero = list(zip(*np.where(board.board != 0)))

        if not non_zero:
            return None

        # 1) 모든 후보 시작점에 대해 사각형을 한 번만 계산 (캐싱)
        rects_cache = {cell: self._enumerate_rects(board, cell) for cell in non_zero}

        # 2) 복합 점수로 랭킹 (높은 점수 = 먼저 시도)
        ranked_starts = sorted(
            non_zero,
            key=lambda cell: self._start_score(board, cell, rows, cols, len(rects_cache[cell])),
            reverse=True
        )

        # 3) 점수 순으로 시작점 시도
        for start in ranked_starts[: self.max_retries]:
            candidates = rects_cache[start]
            if not candidates:
                continue

            best = max(candidates, key=lambda a: self._action_score(board, a))
            return best

        return None  # 모든 후보 시작점에서 실패

    # ------------------------------------------------------------------ #
    #  시작점 점수 (고립위험 + 높은숫자 + 가장자리)
    # ------------------------------------------------------------------ #

    def _start_score(self, board: Board, cell: tuple, rows: int, cols: int, n_rects: int) -> float:
        r, c = cell
        value = int(board.board[r, c])

        # --- 높은 숫자 우선 ---
        value_score = value  # 9가 가장 높음

        # --- 가장자리 우선 ---
        dist_top = r
        dist_bottom = rows - 1 - r
        dist_left = c
        dist_right = cols - 1 - c
        min_dist = min(dist_top, dist_bottom, dist_left, dist_right)
        max_possible = min(rows, cols) // 2
        edge_score = 1.0 - (min_dist / max_possible if max_possible > 0 else 0)

        # --- 고립 위험 (이 칸을 포함하는 합10 사각형이 적을수록 고립 위험 높음) ---
        if n_rects == 0:
            isolation_score = -999  # 이미 고립 -> 선택 의미 없음
        else:
            isolation_score = 1.0 / n_rects

        return (self.w_value * value_score
                + self.w_edge * edge_score
                + self.w_isolation * isolation_score)

    # ------------------------------------------------------------------ #
    #  후보 사각형 열거 (start를 반드시 포함)
    # ------------------------------------------------------------------ #

    def _enumerate_rects(self, board: Board, start: tuple) -> list[Action]:
        r, c = start
        rows, cols = board.size
        candidates = []

        for r1 in range(r + 1):
            for r2 in range(r, rows):
                for c1 in range(c + 1):
                    for c2 in range(c, cols):
                        area = board.get_area(Action((r1, c1), (r2, c2)))
                        s = int(area.sum())

                        if s == 10:
                            candidates.append(Action((r1, c1), (r2, c2)))
                        elif s > 10:
                            break

        return candidates

    # ------------------------------------------------------------------ #
    #  액션(사각형) 점수 - 최종 후보 중 선택용
    # ------------------------------------------------------------------ #

    def _action_score(self, board: Board, action: Action) -> float:
        area = board.get_area(action)
        cell_count = int((area != 0).sum())
        avg_value = float(area[area != 0].mean()) if cell_count > 0 else 0.0

        sim_board = copy.deepcopy(board)
        sim_board.do_action(action)
        future_moves = len(sim_board.get_valid_actions())

        w_cell = 1.0
        w_future = 0.5
        w_avg = -0.3

        return w_cell * cell_count + w_future * future_moves + w_avg * avg_value