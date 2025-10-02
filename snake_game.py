"""Terminal Snake game using curses with an optional demo mode.

Run with ``python snake_game.py`` in a terminal that supports curses for the
interactive experience.  When a fully interactive terminal is unavailable,
use ``python snake_game.py --demo`` to watch an automated preview rendered as
plain text.
"""

from __future__ import annotations

import argparse
import curses
import random
import sys
import time


DIRECTIONS = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
}


def create_food(
    height: int,
    width: int,
    snake: list[tuple[int, int]],
    rng: random.Random | None = None,
) -> tuple[int, int]:
    """Return a random food coordinate not occupied by the snake."""
    available = {(y, x) for y in range(1, height - 1) for x in range(1, width - 1)} - set(snake)
    if not available:
        return -1, -1
    chooser = rng.choice if rng is not None else random.choice
    return chooser(list(available))


def main(stdscr: "curses._CursesWindow") -> None:
    curses.curs_set(False)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    height, width = stdscr.getmaxyx()
    if height < 10 or width < 20:
        stdscr.clear()
        stdscr.addstr(0, 0, "Window too small for Snake. Resize and try again.")
        stdscr.refresh()
        stdscr.getch()
        return

    snake = [(height // 2, width // 2 + i) for i in range(3)][::-1]
    direction = DIRECTIONS[curses.KEY_RIGHT]
    food = create_food(height, width, snake)
    score = 0

    while True:
        stdscr.clear()
        stdscr.border()
        stdscr.addstr(0, 2, f" Score: {score} ")
        if food != (-1, -1):
            stdscr.addch(food[0], food[1], "@")

        for y, x in snake:
            stdscr.addch(y, x, "#")

        stdscr.refresh()

        key = stdscr.getch()
        if key in DIRECTIONS:
            new_direction = DIRECTIONS[key]
            if (new_direction[0] != -direction[0]) or (new_direction[1] != -direction[1]):
                direction = new_direction

        head_y, head_x = snake[0]
        new_head = (head_y + direction[0], head_x + direction[1])

        if (
            new_head[0] in (0, height - 1)
            or new_head[1] in (0, width - 1)
            or new_head in snake
        ):
            break

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = create_food(height, width, snake)
            if food == (-1, -1):
                break
        else:
            snake.pop()

        time.sleep(0.05)

    stdscr.nodelay(False)
    stdscr.addstr(height // 2, width // 2 - 5, "Game Over!")
    stdscr.addstr(height // 2 + 1, width // 2 - 7, f"Final Score: {score}")
    stdscr.addstr(height // 2 + 3, width // 2 - 12, "Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()


def rotate_right(direction: tuple[int, int]) -> tuple[int, int]:
    """Return the direction rotated clockwise."""

    order = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    index = order.index(direction)
    return order[(index + 1) % len(order)]


def render_board(
    height: int,
    width: int,
    snake: list[tuple[int, int]],
    food: tuple[int, int],
    score: int,
) -> str:
    """Render the play field as plain text for demo output."""

    top_bottom = "+" + "-" * (width - 2) + "+"
    rows = [top_bottom]
    body = {(y, x): "O" if i == 0 else "#" for i, (y, x) in enumerate(snake)}

    for y in range(1, height - 1):
        row_chars = ["|"]
        for x in range(1, width - 1):
            if (y, x) == food:
                row_chars.append("@")
            else:
                row_chars.append(body.get((y, x), " "))
        row_chars.append("|")
        rows.append("".join(row_chars))

    rows.append(top_bottom)
    rows.append(f"Score: {score}")
    return "\n".join(rows)


def run_demo(
    *,
    height: int,
    width: int,
    steps: int,
    speed: float,
    seed: int | None,
) -> None:
    """Run an automated Snake preview suitable for non-interactive terminals."""

    rng = random.Random(seed)
    snake = [(height // 2, width // 2 + i) for i in range(3)][::-1]
    direction = (0, 1)
    food = create_food(height, width, snake, rng)
    score = 0

    # Show the initial board before movement.
    print("Demo preview (frame 0):", flush=True)
    print(render_board(height, width, snake, food, score), flush=True)
    print(flush=True)
    if speed > 0:
        time.sleep(speed)

    for frame in range(1, max(steps, 0) + 1):
        for _ in range(4):
            head_y, head_x = snake[0]
            candidate = (head_y + direction[0], head_x + direction[1])
            if (
                0 < candidate[0] < height - 1
                and 0 < candidate[1] < width - 1
                and candidate not in snake
            ):
                break
            direction = rotate_right(direction)
        else:
            break

        snake.insert(0, candidate)

        if candidate == food:
            score += 1
            food = create_food(height, width, snake, rng)
            if food == (-1, -1):
                break
        else:
            snake.pop()

        print(f"Demo preview (frame {frame}):", flush=True)
        print(render_board(height, width, snake, food, score), flush=True)
        print(flush=True)
        if speed > 0:
            time.sleep(speed)

    print("Demo finished. Run without --demo to play interactively.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the Snake game."""

    parser = argparse.ArgumentParser(description="Play Snake in your terminal.")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run an automated plain-text demo instead of the interactive game.",
    )
    parser.add_argument(
        "--demo-height",
        type=int,
        default=20,
        help="Height of the demo board including borders (default: 20).",
    )
    parser.add_argument(
        "--demo-width",
        type=int,
        default=40,
        help="Width of the demo board including borders (default: 40).",
    )
    parser.add_argument(
        "--demo-steps",
        type=int,
        default=60,
        help="Number of demo frames to display (default: 60).",
    )
    parser.add_argument(
        "--demo-speed",
        type=float,
        default=0.15,
        help="Seconds to wait between demo frames (default: 0.15).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed for the random number generator used in demo mode.",
    )
    return parser.parse_args(argv)


def run_cli() -> None:
    """Entry point that handles argument parsing and mode selection."""

    args = parse_args()
    if args.demo:
        run_demo(
            height=max(args.demo_height, 5),
            width=max(args.demo_width, 5),
            steps=args.demo_steps,
            speed=args.demo_speed,
            seed=args.seed,
        )
        return

    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print(
            "Interactive mode requires a TTY-enabled terminal. "
            "Run with --demo for a non-interactive preview.",
        )
        return

    try:
        curses.wrapper(main)
    except curses.error as exc:
        print(
            "Unable to initialize the interactive interface (curses error: "
            f"{exc})."
        )
        print("Run with --demo if your environment does not support curses.")


if __name__ == "__main__":
    run_cli()
