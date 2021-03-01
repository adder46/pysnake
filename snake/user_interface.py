import curses
import sys
import time
from typing import TYPE_CHECKING, Any, Optional

from snake import Window

if TYPE_CHECKING:  # pragma: no cover
    from snake.core import Food, Game, Snake  # pylint: disable=cyclic-import
else:
    Food = Game = Snake = Any


PLAYGROUND_WIDTH = 80
PLAYGROUND_HEIGHT = 24


def ensure_terminal_size() -> bool:
    """
    Helper function to ensure correct terminal size
    """
    if curses.LINES >= PLAYGROUND_HEIGHT and curses.COLS >= PLAYGROUND_WIDTH:
        return True
    return False

def make_color_pairs() -> None:
    """
    Helper function to make curses color pairs
    """
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)

def create_screen(stdscr: Window) -> Optional[Window]:
    if ensure_terminal_size():
        inner_screen = stdscr.subwin(
            PLAYGROUND_HEIGHT,
            PLAYGROUND_WIDTH,
            (curses.LINES - PLAYGROUND_HEIGHT) // 2,
            (curses.COLS - PLAYGROUND_WIDTH) // 2,
        )
        return inner_screen
    return None


class UserInterface:
    def __init__(self, screen: Window):
        self.screen = screen

    def render_snake(self, snake: Snake) -> None:
        """
        Draws the body, piece by piece, colored white.
        """
        for piece in snake.body:
            self.screen.addstr(piece.y, piece.x * 2, "  ", curses.color_pair(1))

    def render_food(self, food: Food) -> None:
        """
        Draws the food at [Y, X] coords, colored red.
        """
        self.screen.addstr(food.coord.y, food.coord.x * 2, "  ", curses.color_pair(2))

    def render_score(self, score: int) -> None:
        """
        Displays current score at the lower left-hand side of the screen.
        """
        self.screen.addstr(PLAYGROUND_HEIGHT - 1, 2, f" SCORE: {score} ", curses.A_BOLD)
