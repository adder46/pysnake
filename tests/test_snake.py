import pytest
from snake import core
from tests.fixtures import fake_stdscr


@pytest.mark.parametrize(
    "current, potential",
    [
        ["up", [("left", (0, -1)), ("right", (0, 1))]],
        ["down", [("left", (0, -1)), ("right", (0, 1))]],
        ["left", [("up", (-1, 0)), ("down", (1, 0))]],
        ["right", [("up", (-1, 0)), ("down", (1, 0))]],
    ],
)
def test_move(current, potential, fake_stdscr):
    game = core.Game(fake_stdscr)
    if current == "left":
        game.set_direction_if_possible("up")
        for _ in range(5):
            game.snake.move()
    for direction, (y, x) in potential:
        game.snake.direction = current
        game.snake.move()
        before = game.snake.body.copy()
        game.set_direction_if_possible(direction)
        game.snake.move()
        assert game.snake.body[-1][0] == before[-1][0] + y
        assert game.snake.body[-1][1] == before[-1][1] + x


def test_eat_food(fake_stdscr):
    snake = core.Snake(fake_stdscr)
    before_eating = len(snake.body)
    snake.eat_food()
    assert len(snake.body) == before_eating + 1


def test_is_touching_food(fake_stdscr):
    game = core.Game(fake_stdscr)
    game.food.x = game.snake.body[-1][1] + 1
    game.food.y = game.snake.body[-1][0]
    assert not game.snake.is_touching_food(game.food)
    game.snake.move()
    assert game.snake.is_touching_food(game.food)


@pytest.mark.parametrize(
    "direction, coords",
    [
        ["up", [11, 23]],
        ["down", [13, 23]],
        ["left", [12, 24]],
        ["right", [12, 24]],
    ],
)
def test_get_next_step(direction, coords, fake_stdscr):
    game = core.Game(fake_stdscr)
    game.set_direction_if_possible(direction)
    assert game.snake.get_next_step() == coords


def test_collision(fake_stdscr):
    game = core.Game(fake_stdscr)
    for direction in ("right", "up", "left", "down"):
        game.set_direction_if_possible(direction)
        if direction == "down":
            with pytest.raises(core.CollisionError):
                game.snake.move()
        else:
            game.snake.move()
