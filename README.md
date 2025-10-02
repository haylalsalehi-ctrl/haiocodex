# haiocodex

This repository now contains a simple terminal-based Snake game implemented in Python.

## Running the game

1. Ensure you are in a terminal that supports `curses` (most Unix-like terminals do).
2. Run the game with:

   ```bash
   python snake_game.py
   ```

Use the arrow keys to control the snake. Eat the `@` food items to grow and increase your score. Avoid running into the walls or the snake's own body.

## Development notes

- Tests: `pytest -q`
- Lint: `ruff .`
- Build: `npm run build`
- Conventions: follow Black + Ruff; open PRs to branch `codex/*`.
