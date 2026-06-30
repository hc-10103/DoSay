"""
실험: 시작점 선택 전략 비교
  - random : 완전 랜덤 시작점
  - smart  : 고립위험 + 높은숫자 + 가장자리 복합 점수

여러 번 시뮬레이션 돌려서 평균 제거 칸 수 / 클리어율 비교
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import numpy as np
from game import Board, Action
from greedy import GreedyAgent
import copy as copy_module

def _action_score(self, board, action):
    area = board.get_area(action)
    cell_count = int((area != 0).sum())
    avg_value = float(area[area != 0].mean()) if cell_count > 0 else 0.0

    # board.py 안 건드리고 deepcopy로 우회
    sim_board = copy_module.deepcopy(board)
    sim_board.do_action(action)
    future_moves = len(sim_board.get_valid_actions())

    return 1.0 * cell_count + 0.5 * future_moves - 0.3 * avg_value

class RandomStartAgent:
    """비교 baseline: 완전 랜덤 시작점 (기존 버전)"""

    def __init__(self, max_retries: int = 30):
        self.max_retries = max_retries

    def select_action(self, board: Board):
        non_zero = list(zip(*np.where(board.board != 0)))
        if not non_zero:
            return None

        tried = set()
        for _ in range(self.max_retries):
            start = random.choice(non_zero)
            if start in tried:
                continue
            tried.add(start)

            candidates = self._enumerate_rects(board, start)
            if not candidates:
                continue

            return max(candidates, key=lambda a: self._action_score(board, a))

        return None

    def _enumerate_rects(self, board, start):
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

    def _action_score(self, board, action):
        area = board.get_area(action)
        cell_count = int((area != 0).sum())
        avg_value = float(area[area != 0].mean()) if cell_count > 0 else 0.0
        sim_board = copy_module.deepcopy(board)
        sim_board.do_action(action)
        future_moves = len(sim_board.get_valid_actions())
        return 1.0 * cell_count + 0.5 * future_moves - 0.3 * avg_value


def run_episode(agent, seed: int) -> dict:
    np.random.seed(seed)
    random.seed(seed)
    board = Board()

    step = 0
    removed_cells = 0
    is_all_clear = False

    while True:
        is_over, is_all_clear = board.is_done()
        if is_all_clear or is_over:
            break

        action = agent.select_action(board)
        if action is None:
            break

        area = board.get_area(action)
        removed_cells += int((area != 0).sum())
        board.do_action(action)
        step += 1

    return {"steps": step, "removed": removed_cells, "all_clear": is_all_clear}


def run_experiment(n_trials: int = 20):
    results = {"random": [], "smart": []}

    for i in range(n_trials):
        seed = i

        # 같은 시드 -> 같은 초기 보드로 양쪽 비교
        random_agent = RandomStartAgent(max_retries=50)
        smart_agent = GreedyAgent(max_retries=50, w_value=1.0, w_edge=1.0, w_isolation=1.0)

        results["random"].append(run_episode(random_agent, seed))
        results["smart"].append(run_episode(smart_agent, seed))

    print(f"\n{'='*60}")
    print(f"  실험 결과 ({n_trials}회 시뮬레이션)")
    print(f"{'='*60}\n")

    for name, runs in results.items():
        avg_removed = np.mean([r["removed"] for r in runs])
        avg_steps = np.mean([r["steps"] for r in runs])
        clear_rate = np.mean([r["all_clear"] for r in runs]) * 100

        print(f"[{name:>7}] 평균 제거 칸수: {avg_removed:6.1f}  "
              f"평균 스텝: {avg_steps:5.1f}  클리어율: {clear_rate:5.1f}%")

    print()
    return results


if __name__ == "__main__":
    run_experiment(n_trials=20)