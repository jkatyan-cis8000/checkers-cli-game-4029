from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Player(Enum):
    RED = "red"
    BLACK = "black"


@dataclass
class Position:
    row: int
    col: int


@dataclass
class Piece:
    color: Player
    is_king: bool


@dataclass
class Move:
    from_pos: Position
    to_pos: Position
    captured: List[Position]


class BoardState:
    def __init__(self) -> None:
        self._grid: List[List[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def get(self, row: int, col: int) -> Optional[Piece]:
        return self._grid[row][col]

    def set(self, row: int, col: int, piece: Optional[Piece]) -> None:
        self._grid[row][col] = piece

    def copy(self) -> "BoardState":
        new_board = BoardState()
        for row in range(8):
            for col in range(8):
                new_board._grid[row][col] = self._grid[row][col]
        return new_board

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BoardState):
            return False
        for row in range(8):
            for col in range(8):
                if self._grid[row][col] != other._grid[row][col]:
                    return False
        return True
