"""Repository module for board persistence."""

import json
from pathlib import Path

from types.types import BoardState, Piece, Player


def save_board(board: BoardState, filename: str) -> None:
    """Save board state to JSON file."""
    path = Path(filename)
    data = {
        "rows": [
            [
                _piece_to_dict(board.get(r, c)) if board.get(r, c) else None
                for c in range(8)
            ]
            for r in range(8)
        ]
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_board(filename: str) -> BoardState:
    """Load board state from JSON file."""
    path = Path(filename)
    with open(path, "r") as f:
        data = json.load(f)

    board = BoardState()
    for r, row_data in enumerate(data["rows"]):
        for c, piece_data in enumerate(row_data):
            if piece_data is not None:
                board.set(r, c, _dict_to_piece(piece_data))
    return board


def _piece_to_dict(piece) -> dict:
    """Convert Piece to JSON-compatible dict."""
    return {
        "color": piece.color.value,
        "is_king": piece.is_king,
    }


def _dict_to_piece(data: dict):
    """Convert JSON dict to Piece."""
    color = Player.RED if data["color"] == "red" else Player.BLACK
    return Piece(color=color, is_king=data["is_king"])


def initialize_board() -> BoardState:
    """Create a new board with starting position."""
    board = BoardState()
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board.set(row, col, Piece(color=Player.RED, is_king=False))
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board.set(row, col, Piece(color=Player.BLACK, is_king=False))
    return board
