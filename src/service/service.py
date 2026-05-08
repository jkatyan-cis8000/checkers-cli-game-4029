from typing import List

from ..types.types import BoardState, Move, Piece, Player


def validate_move(board: BoardState, move: Move, current_player: Player) -> bool:
    from_pos = move.from_pos
    to_pos = move.to_pos

    piece = board.get(from_pos.row, from_pos.col)
    if piece is None:
        return False
    if piece.color != current_player:
        return False

    if board.get(to_pos.row, to_pos.col) is not None:
        return False

    row_diff = to_pos.row - from_pos.row
    col_diff = to_pos.col - from_pos.col

    if piece.is_king:
        if abs(row_diff) != abs(col_diff):
            return False
    else:
        direction = 1 if current_player == Player.RED else -1
        if row_diff != direction and row_diff != 2 * direction:
            return False
        if abs(col_diff) != abs(row_diff):
            return False

    if abs(row_diff) == 2:
        mid_row = (from_pos.row + to_pos.row) // 2
        mid_col = (from_pos.col + to_pos.col) // 2
        captured = board.get(mid_row, mid_col)
        if captured is None or captured.color == current_player:
            return False
        if mid_row not in move.captured:
            return False

    return True


def apply_move(board: BoardState, move: Move) -> BoardState:
    new_board = board.copy()
    from_pos = move.from_pos
    to_pos = move.to_pos

    piece = new_board.get(from_pos.row, from_pos.col)
    new_board.set(from_pos.row, from_pos.col, None)

    new_board.set(to_pos.row, to_pos.col, piece)

    for captured_pos in move.captured:
        new_board.set(captured_pos.row, captured_pos.col, None)

    return new_board


def check_kinging(move: Move) -> bool:
    to_pos = move.to_pos
    return to_pos.row == 0 or to_pos.row == 7


def _get_piece_direction(player: Player) -> int:
    return 1 if player == Player.RED else -1


def _has_simple_move(board: BoardState, player: Player, row: int, col: int) -> bool:
    piece = board.get(row, col)
    if piece is None or piece.color != player:
        return False

    direction = _get_piece_direction(player)

    for dr in [-direction, direction]:
        for dc in [-1, 1]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board.get(new_row, new_col) is None:
                    return True

    if piece.is_king:
        for dr in [-1, 1]:
            for dc in [-1, 1]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if board.get(new_row, new_col) is None:
                        return True

    return False


def _has_capture_move(board: BoardState, player: Player, row: int, col: int) -> bool:
    piece = board.get(row, col)
    if piece is None or piece.color != player:
        return False

    directions = [-1, 1] if piece.is_king else [_get_piece_direction(player)]

    for dr in directions:
        for dc in [-1, 1]:
            mid_row, mid_col = row + dr, col + dc
            jump_row, jump_col = row + 2 * dr, col + 2 * dc

            if 0 <= jump_row < 8 and 0 <= jump_col < 8:
                mid_piece = board.get(mid_row, mid_col)
                if mid_piece is not None and mid_piece.color != player:
                    if board.get(jump_row, jump_col) is None:
                        return True

    if piece.is_king:
        for dr in [-1, 1]:
            for dc in [-1, 1]:
                for dist in range(1, 8):
                    mid_row, mid_col = row + dr * dist, col + dc * dist
                    jump_row, jump_col = row + dr * (dist + 1), col + dc * (dist + 1)

                    if not (0 <= jump_row < 8 and 0 <= jump_col < 8):
                        break

                    mid_piece = board.get(mid_row, mid_col)
                    if mid_piece is not None:
                        if mid_piece.color != player and board.get(jump_row, jump_col) is None:
                            return True
                        break

    return False


def has_valid_moves(board: BoardState, player: Player) -> bool:
    for row in range(8):
        for col in range(8):
            if _has_simple_move(board, player, row, col):
                return True
            if _has_capture_move(board, player, row, col):
                return True
    return False
