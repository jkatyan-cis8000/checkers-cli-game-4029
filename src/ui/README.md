# UI Layer

User-facing surfaces - CLI, web, GUI.

## What belongs here

- CLI rendering of board state
- Move input parsing (e.g., "e2-e4")
- User prompts and messages
- Game status display

## What does NOT belong here

- Game rules (use service layer)
- Data persistence (use repo layer)
- Core business logic
