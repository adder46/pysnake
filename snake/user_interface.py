import curses
import sys
from typing import TYPE_CHECKING, Any, Optional

import trio

from snake import Window

if TYPE_CHECKING:
    from snake.core import Food, Game, Snake  # pylint: disable=cyclic-import
else:
    Food = Game = Snake = Any


PLAYGROUND_WIDTH = 80
PLAYGROUND_HEIGHT = 24


class UserInterface:
    def __init__(self, screen: Window):
        self.screen = screen
        self.renderer = Renderer(screen)
        self.make_color_pairs()

    @staticmethod
    def ensure_terminal_size() -> bool:
        """
        Helper method to ensure correct terminal size
        """
        if curses.LINES >= PLAYGROUND_HEIGHT and curses.COLS >= PLAYGROUND_WIDTH:
            return True
        return False

    @staticmethod
    def make_color_pairs() -> None:
        """
        Helper method to make curses color pairs
        """
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)

    async def display_game_over_screen(self, game: Game) -> None:
        """
        Displays game over screen and waits for user input.
        If the input are keys "q" or "r", it quits or restarts the game, respectively.
        """
        self.screen.erase()
        self.screen.addstr(
            PLAYGROUND_HEIGHT // 2 - 1, PLAYGROUND_WIDTH // 2 - 4, "GAME OVER"
        )
        self.screen.addstr(
            PLAYGROUND_HEIGHT // 2, PLAYGROUND_WIDTH // 2 - 4, f"SCORE: {game.score}"
        )
        self.screen.addstr(
            PLAYGROUND_HEIGHT // 2 + 2, PLAYGROUND_WIDTH // 2 - 7, "[r]estart [q]uit"
        )

        self.screen.refresh()

        while True:
            try:
                user_input = self.screen.getch()
            except curses.error:
                await trio.sleep(0.1)
                continue
            if ord("q") == user_input:
                sys.exit()
            if ord("r") == user_input:
                game.restart()
                break

    def display_score(self, score: int) -> None:
        """
        Displays current score at the lower left-hand side of the screen.
        """
        self.screen.addstr(PLAYGROUND_HEIGHT - 1, 2, f" SCORE: {score} ", curses.A_BOLD)


class Renderer:
    def __init__(self, screen: Window):
        self.screen = screen

    def render_snake(self, snake: Snake) -> None:
        """
        Draws the body, piece by piece, colored white.
        """
        for piece in snake.body:
            self.screen.addstr(piece[0], piece[1] * 2, "  ", curses.color_pair(1))

    def render_food(self, food: Food) -> None:
        """
        Draws the food at [Y, X] coords, colored red.
        """
        self.screen.addstr(food.y, food.x * 2, "  ", curses.color_pair(2))


def create_screen(stdscr: Window) -> Optional[Window]:
    if UserInterface.ensure_terminal_size():
        inner_screen = stdscr.subwin(
            PLAYGROUND_HEIGHT,
            PLAYGROUND_WIDTH,
            (curses.LINES - PLAYGROUND_HEIGHT) // 2,
            (curses.COLS - PLAYGROUND_WIDTH) // 2,
        )
        return inner_screen
    return None
