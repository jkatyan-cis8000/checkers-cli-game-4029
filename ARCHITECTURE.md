# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.
Update it when the structure changes; do not let it drift from the actual code.

## Module Structure

- src/types.py: Pure type definitions for Checkers (Piece, Player, BoardState, Move, Position)
- src/config.py: Game constants (BOARD_SIZE=8, PLAYER_COLORS, etc.)
- src/repo.py: Board persistence (save/load board state)
- src/service.py: Game rules - move validation, capture logic, kinging rules
- src/runtime.py: Game loop orchestration, turn management
- src/ui.py: CLI rendering, move input parsing (e.g., "e2-e4")
- src/providers/flags.py: Feature flags (if needed)
- src/utils.py: Pure helpers (position conversion, string parsing)

## Interfaces

### types.py
- `Piece` class: color (Player.RED/Player.BLACK), is_king (bool)
- `Player` enum: RED, BLACK
- `Position` class: row, col (0-7)
- `Move` class: from_pos, to_pos, captured (list of Position)
- `BoardState` class: 8x8 grid of Optional[Piece]

### config.py
- `BOARD_SIZE = 8`
- `PLAYER_COLORS = {Player.RED: 'R', Player.BLACK: 'B'}`
- `INITIAL_BOARD_CONFIG`: starting piece positions

### service.py
- `validate_move(board, move, current_player) -> bool`: Checkers rules
- `apply_move(board, move) -> BoardState`: Execute move with captures
- `check_kinging(move) -> bool`: Did piece reach opponent's back row?
- `has_valid_moves(board, player) -> bool`: Check if player can move

### ui.py
- `render_board(board) -> str`: ASCII board with pieces
- `parse_move_input(input_str) -> Move | None`: Parse "e2-e4" notation
- `get_player_input() -> str`: Read move from stdin

### runtime.py
- `run_game() -> None`: Main loop - display, input, validate, update

## Shared Data Structures

**Piece**: `{color: 'red'|'black', is_king: bool}`
**Position**: `{row: int (0-7), col: int (0-7)}`
**Move**: `{from_pos: Position, to_pos: Position, captured: [Position]}`

## External Dependencies

None - pure Python implementation.
