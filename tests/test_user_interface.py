import pytest

from snake import core
from snake import user_interface
from tests.fixtures import fake_curses, fake_stdscr
from tests.util import fake_getch_game_over


def test_ensure_terminal_size(fake_curses, fake_stdscr):
    assert user_interface.ensure_terminal_size()
    fake_curses.LINES = 10
    fake_curses.COLS = 60
    assert not user_interface.ensure_terminal_size()


def test_render_snake(fake_curses, fake_stdscr):
    game = core.Game(fake_stdscr)
    ui = user_interface.UserInterface(fake_stdscr)
    ui.render_snake(game.snake)
    for piece in game.snake.body:
        assert (piece.y, piece.x * 2, "  ", None) in fake_stdscr.addstred


def test_render_food(fake_curses, fake_stdscr):
    game = core.Game(fake_stdscr)
    ui = user_interface.UserInterface(fake_stdscr)
    ui.render_food(game.food)
    assert (
        game.food.coord.y,
        game.food.coord.x * 2,
        "  ",
        None,
    ) in fake_stdscr.addstred


def test_render_score(fake_curses, fake_stdscr):
    ui = user_interface.UserInterface(fake_stdscr)
    ui.render_score("100")
    assert (
        user_interface.PLAYGROUND_HEIGHT - 1,
        2,
        " SCORE: 100 ",
        None,
    ) in fake_stdscr.addstred
