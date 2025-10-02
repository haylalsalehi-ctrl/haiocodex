"""Terminal Snake game using curses.

Run with `python snake_game.py` in a terminal that supports curses.
"""

import curses
import random
import time


DIRECTIONS = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
}


def create_food(height: int, width: int, snake: list[tuple[int, int]]) -> tuple[int, int]:
    """Return a random food coordinate not occupied by the snake."""
    available = {(y, x) for y in range(1, height - 1) for x in range(1, width - 1)} - set(snake)
    if not available:
        return -1, -1
    return random.choice(list(available))


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


if __name__ == "__main__":
    curses.wrapper(main)
