# haiocodex

This repository now contains a simple terminal-based Snake game implemented in Python.

## Running the game

1. Ensure you are in a terminal that supports `curses` (most Unix-like terminals do).
2. Run the game with:

   ```bash
   python snake_game.py
   ```

Use the arrow keys to control the snake. Eat the `@` food items to grow and increase your score. Avoid running into the walls or the snake's own body.

If you are in an environment without full terminal capabilities (such as some CI systems), you can still see the game in action by running the automated text-mode demo:

```bash
python snake_game.py --demo
```

Additional flags like `--demo-steps`, `--demo-speed`, `--demo-height`, and `--demo-width` let you tweak the preview.

## Development notes

- Tests: `pytest -q`
- Lint: `ruff .`
- Build: `npm run build`
- Conventions: follow Black + Ruff; open PRs to branch `codex/*`.
