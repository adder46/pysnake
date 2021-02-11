import pytest
from snake import core
from tests.fixtures import fake_curses, fake_stdscr
from tests.util import fake_getch_pause


async def test_pause(monkeypatch, fake_curses, fake_stdscr):
    monkeypatch.setattr(fake_stdscr, "getch", fake_getch_pause)
    game = core.Game(fake_stdscr)
    snake_before = game.snake.body
    await game.pause()
    assert game.snake.body == snake_before


def test_restart(fake_stdscr):
    game = core.Game(fake_stdscr)
    game.restart()
    assert game.food_counter == 0 and game.score == 0


@pytest.mark.parametrize(
    "current, wanted",
    [["right", "left"], ["left", "right"], ["up", "down"], ["down", "up"]],
)
def test_set_direction_if_possible(current, wanted, fake_stdscr):
    game = core.Game(fake_stdscr)
    game.snake.direction = current
    assert game.set_direction_if_possible(wanted) is None


@pytest.mark.parametrize(
    "current, valid",
    [
        ["up", ["left", "right"]],
        ["down", ["left", "right"]],
        ["left", ["up", "down"]],
        ["right", ["up", "down"]],
    ],
)
def test_set_direction_if_possible_valid(current, valid, fake_stdscr):
    game = core.Game(fake_stdscr)
    for direction in valid:
        game.snake.direction = current
        game.set_direction_if_possible(direction)
        assert game.snake.direction == direction


@pytest.mark.parametrize(
    "before, after",
    [
        [0, 1],
        [23, 24],
        [99, 0],
    ],
)
def test_handle_food_counter(before, after, fake_stdscr):
    game = core.Game(fake_stdscr)
    game.food_counter = before
    game.handle_food()
    assert game.food_counter == after


def test_handle_food_updating_score(fake_stdscr):
    game = core.Game(fake_stdscr)
    game.food.y = game.snake.body[-1][0]
    game.food.x = game.snake.body[-1][1] + 1
    game.snake.move()
    game.handle_food()
    assert game.score == 1 and game.food_counter == 0
