"""Configuration constants for the Checkers game."""

from ..types.types import Player

BOARD_SIZE = 8

PLAYER_COLORS = {
    Player.RED: 'R',
    Player.BLACK: 'B'
}

PLAYER_NAMES = {
    Player.RED: 'Red',
    Player.BLACK: 'Black'
}

STARTING_POSITIONS: dict[tuple[int, int], Player] = {}

for row in range(3):
    for col in range(8):
        if (row + col) % 2 == 1:
            STARTING_POSITIONS[(row, col)] = Player.RED

for row in range(5, 8):
    for col in range(8):
        if (row + col) % 2 == 1:
            STARTING_POSITIONS[(row, col)] = Player.BLACK
