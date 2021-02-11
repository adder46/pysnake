from snake import core
from tests.fixtures import fake_stdscr


def test_food_does_not_overlap_Snake(fake_stdscr):
    snake = core.Snake(fake_stdscr)
    food = core.Food(fake_stdscr, snake.body)
    assert not food.is_overlapping_snake(snake.body)


def test_food_overlaps_Snake(fake_stdscr):
    snake = core.Snake(fake_stdscr)
    food = core.Food(fake_stdscr, snake.body)
    food.y = snake.body[3][0]
    food.x = snake.body[3][1]
    assert food.is_overlapping_snake(snake.body)
