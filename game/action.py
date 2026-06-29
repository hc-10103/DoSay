from dataclasses import dataclass

@dataclass
class Action:
    start: tuple[int, int]
    end: tuple[int, int]