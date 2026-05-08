from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Position:
    row: int
    col: int


def algebraic_to_position(algebraic: str) -> Optional[Position]:
    """Parse algebraic notation like 'e2' into Position(row, col).
    
    Columns a-h map to 0-7.
    Rows 1-8 map to 7-0 (row 1 is bottom row = index 7).
    Returns None if invalid format.
    """
    if not is_valid_algebraic(algebraic):
        return None
    
    col_char = algebraic[0]
    row_char = algebraic[1]
    
    col = ord(col_char) - ord('a')
    row = 8 - int(row_char)
    
    return Position(row=row, col=col)


def position_to_algebraic(pos: Position) -> str:
    """Convert Position to algebraic notation like 'e2'.
    
    Column 0-7 maps to a-h.
    Row 0-7 maps to 8-1 (row 0 is top row = '8').
    """
    col_char = chr(ord('a') + pos.col)
    row_char = str(8 - pos.row)
    
    return f"{col_char}{row_char}"


def parse_move_input(input_str: str) -> Optional[Tuple[Position, Position]]:
    """Parse move input like 'e2-e4' into (from_pos, to_pos).
    
    Returns None if input format is invalid.
    """
    if not isinstance(input_str, str):
        return None
    
    parts = input_str.split('-')
    
    if len(parts) != 2:
        return None
    
    from_pos = algebraic_to_position(parts[0].strip())
    to_pos = algebraic_to_position(parts[1].strip())
    
    if from_pos is None or to_pos is None:
        return None
    
    return (from_pos, to_pos)


def is_valid_algebraic(s: str) -> bool:
    """Check if string is valid algebraic notation (like 'e2', 'a1', 'h8').
    
    Valid format: letter a-h followed by digit 1-8.
    """
    if not isinstance(s, str):
        return False
    
    if len(s) != 2:
        return False
    
    col_char = s[0]
    row_char = s[1]
    
    if col_char not in 'abcdefgh':
        return False
    
    if row_char not in '12345678':
        return False
    
    return True


def get_square_color(row: int, col: int) -> str:
    """Return 'black' or 'white' for the given square.
    
    Row 0 is top row, col 0 is left column.
    """
    if (row + col) % 2 == 0:
        return 'white'
    else:
        return 'black'
