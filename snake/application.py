import curses
import sys
from typing import Optional

import trio

from snake import Window
from snake.core import Game, CollisionError
from snake.user_interface import (
    PLAYGROUND_HEIGHT,
    PLAYGROUND_WIDTH,
    UserInterface,
    create_screen,
)


DIRECTIONS = {
    curses.KEY_UP: "up",
    curses.KEY_DOWN: "down",
    curses.KEY_LEFT: "left",
    curses.KEY_RIGHT: "right",
}


def sync_main() -> None:
    curses.wrapper(lambda stdscr: trio.run(main, stdscr))  # pragma: no cover


async def main(stdscr: Window) -> None:
    stdscr.nodelay(True)
    curses.curs_set(False)

    inner_screen = create_screen(stdscr)
    assert inner_screen is not None

    stdscr.timeout(100)

    user_interface = UserInterface(inner_screen)
    game = Game(inner_screen)

    while True:
        stdscr.erase()
        inner_screen.erase()
        inner_screen.box(0, 0)

        user_interface.renderer.render_snake(game.snake)
        game.handle_food()
        user_interface.renderer.render_food(game.food)
        user_interface.display_score(game.score)

        stdscr.refresh()
        inner_screen.refresh()

        try:
            game.snake.move()
        except CollisionError:
            await user_interface.display_game_over_screen(game)

        try:
            user_input = stdscr.getch()
        except curses.error:
            continue
        except KeyboardInterrupt:  # pragma: no cover
            sys.exit()

        if user_input in DIRECTIONS:
            game.set_direction_if_possible(DIRECTIONS[user_input])

        if user_input == ord("p"):
            await game.pause()

        if user_input == ord("q"):
            sys.exit()
