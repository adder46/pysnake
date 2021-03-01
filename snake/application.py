import curses
import sys

from snake import Window
from snake.core import (
    CollisionError,
    Direction,
    Game,
)
from snake.user_interface import (
    PLAYGROUND_HEIGHT,
    PLAYGROUND_WIDTH,
    UserInterface,
    create_screen,
    make_color_pairs,
)


DIRECTIONS = {
    curses.KEY_UP: Direction.UP,
    curses.KEY_DOWN: Direction.DOWN,
    curses.KEY_LEFT: Direction.LEFT,
    curses.KEY_RIGHT: Direction.RIGHT,
}


def main(stdscr: Window) -> None:
    stdscr.nodelay(True)
    curses.curs_set(False)

    inner_screen = create_screen(stdscr)
    assert inner_screen is not None

    make_color_pairs()

    stdscr.timeout(100)
    stdscr.keypad(True)

    user_interface = UserInterface(inner_screen)
    game = Game(inner_screen)

    while True:
        stdscr.erase()
        inner_screen.erase()
        inner_screen.box(0, 0)

        user_interface.render_snake(game.snake)
        game.handle_food()
        user_interface.render_food(game.food)
        user_interface.render_score(game.score)

        stdscr.refresh()
        inner_screen.refresh()

        if not game.paused:
            try:
                game.snake.move()
            except CollisionError:  # pragma: no cover
                break

        try:
            user_input = stdscr.getch()
        except curses.error:
            continue
        except KeyboardInterrupt:  # pragma: no cover
            sys.exit()

        if user_input in DIRECTIONS:
            game.set_direction(DIRECTIONS[user_input])

        elif user_input == ord("p"):
            game.pause()

        elif user_input == ord("q"):
            sys.exit()
