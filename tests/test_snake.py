import pytest
from snake import core
from tests.fixtures import fake_stdscr


@pytest.mark.parametrize(
    "current, potential",
    [
        [
            core.Direction.UP, [
                (core.Direction.LEFT, core.Coord(0, -1)),
                (core.Direction.RIGHT, core.Coord(0, 1))
            ]
        ],
        [
            core.Direction.DOWN, [
                (core.Direction.LEFT, core.Coord(0, -1)),
                (core.Direction.RIGHT, core.Coord(0, 1))
            ]
        ],
        [
            core.Direction.LEFT, [
                (core.Direction.UP, core.Coord(-1, 0)),
                (core.Direction.DOWN, core.Coord(1, 0))
            ]
        ],
        [
            core.Direction.RIGHT, [
                (core.Direction.UP, core.Coord(-1, 0)),
                (core.Direction.DOWN, core.Coord(1, 0))
            ]
        ],
    ],
)
def test_move(current, potential, fake_stdscr):
    game = core.Game(fake_stdscr)
    if current == core.Direction.LEFT:
        game.set_direction_if_possible(core.Direction.UP)
        for _ in range(5):
            game.snake.move()
    for direction, next_step in potential:
        game.snake.direction = current
        game.snake.move()
        before = game.snake.body.copy()
        game.set_direction_if_possible(direction)
        game.snake.move()
        assert game.snake.body[-1] == before[-1] + next_step


def test_eat_food(fake_stdscr):
    snake = core.Snake(fake_stdscr)
    before_eating = len(snake.body)
    snake.eat_food()
    assert len(snake.body) == before_eating + 1


def test_is_touching_food(fake_stdscr):
    game = core.Game(fake_stdscr)
    game.food.coord.y = game.snake.body[-1].y
    game.food.coord.x = game.snake.body[-1].x + 1
    assert not game.snake.is_touching_food(game.food)
    game.snake.move()
    assert game.snake.is_touching_food(game.food)


@pytest.mark.parametrize(
    "direction, coords",
    [
        [core.Direction.UP, core.Coord(y=11, x=23)],
        [core.Direction.DOWN, core.Coord(y=13, x=23)],
        [core.Direction.LEFT, core.Coord(y=12, x=24)],
        [core.Direction.RIGHT, core.Coord(y=12, x=24)],
    ],
)
def test_get_next_step(direction, coords, fake_stdscr):
    game = core.Game(fake_stdscr)
    game.set_direction_if_possible(direction)
    assert game.snake.get_next_step() == coords


def test_collision(fake_stdscr):
    game = core.Game(fake_stdscr)
    for direction in (
        core.Direction.RIGHT,
        core.Direction.UP,
        core.Direction.LEFT,
        core.Direction.DOWN,
    ):
        game.set_direction_if_possible(direction)
        if direction == core.Direction.DOWN:
            with pytest.raises(core.CollisionError):
                game.snake.move()
        else:
            game.snake.move()
