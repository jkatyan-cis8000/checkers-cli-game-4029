from ..types.types import BoardState, Move, Player
from ..config.config import BOARD_SIZE


def render_board(board: BoardState) -> str:
    lines = []
    lines.append("  a b c d e f g h")
    for row in range(BOARD_SIZE):
        line = f"{BOARD_SIZE - row} "
        for col in range(BOARD_SIZE):
            piece = board.get(row, col)
            if piece is None:
                line += ". "
            else:
                symbol = piece.color.value[0].upper()
                if piece.is_king:
                    symbol = symbol.lower()
                line += f"{symbol} "
        lines.append(line)
    return "\n".join(lines)


def parse_move_input(input_str: str) -> Move | None:
    try:
        parts = input_str.strip().split("-")
        if len(parts) != 2:
            return None
        from_pos = _parse_position(parts[0])
        to_pos = _parse_position(parts[1])
        if from_pos is None or to_pos is None:
            return None
        return Move(from_pos=from_pos, to_pos=to_pos, captured=[])
    except Exception:
        return None


def _parse_position(pos_str: str) -> Position | None:
    if len(pos_str) != 2:
        return None
    col_char = pos_str[0]
    row_char = pos_str[1]
    if col_char < "a" or col_char > "h":
        return None
    if row_char < "1" or row_char > "8":
        return None
    col = ord(col_char) - ord("a")
    row = BOARD_SIZE - int(row_char)
    from ..types.types import Position
    return Position(row=row, col=col)


def display_game_state(board: BoardState, current_player: Player) -> None:
    print(render_board(board))
    print(f"Current player: {current_player.value}")
