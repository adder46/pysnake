import pytest

from snake import core
from snake import user_interface
from tests.fixtures import fake_curses, fake_stdscr


def test_render_snake(fake_curses, fake_stdscr):
    game = core.Game(fake_stdscr)
    renderer = user_interface.Renderer(fake_stdscr)
    renderer.render_snake(game.snake)
    for piece in game.snake.body:
        assert (piece[0], piece[1] * 2, "  ", None) in fake_stdscr.addstred


def test_render_food(fake_curses, fake_stdscr):
    game = core.Game(fake_stdscr)
    renderer = user_interface.Renderer(fake_stdscr)
    renderer.render_food(game.food)
    assert (
        game.food.y_coord,
        game.food.x_coord * 2,
        "  ",
        None,
    ) in fake_stdscr.addstred
