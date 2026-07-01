from .board import Board


def rect_sum(sum_prefix, r1, c1, r2, c2) -> int:
    return (sum_prefix[r2 + 1, c2 + 1]
            - sum_prefix[r1, c2 + 1]
            - sum_prefix[r2 + 1, c1]
            + sum_prefix[r1, c1])

def _get_apple_count(cnt_prefix, r1, c1, r2, c2) -> int:
    return (cnt_prefix[r2 + 1, c2 + 1]
        - cnt_prefix[r1, c2 + 1]
        - cnt_prefix[r2 + 1, c1]
        + cnt_prefix[r1, c1])

def has_apple_in_row(cnt_prefix, r, c1, c2) -> bool:
    return _get_apple_count(cnt_prefix, r, c1, r, c2) > 0

def has_apple_in_col(cnt_prefix, c, r1, r2) -> bool:
    return _get_apple_count(cnt_prefix, r1, c, r2, c) > 0