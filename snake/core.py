import collections
import curses
import enum
import random
from typing import (
    Any,
    Dict,
    Deque,
    Optional
)

import attr
import trio

from snake import Window
from snake.user_interface import PLAYGROUND_HEIGHT, PLAYGROUND_WIDTH


@attr.s
class Coord:
    y: int = attr.ib()
    x: int = attr.ib()

    def __add__(self, other):
        return Coord(self.y + other.y, self.x + other.x)


class Direction(enum.Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


DIRECTIONS: Dict[Direction, Any] = {
    Direction.UP: {
        "coords": Coord(x=0, y=-1),
        "forbidden": Direction.DOWN
    },
    Direction.DOWN: {
        "coords": Coord(x=0, y=1),
        "forbidden": Direction.UP
    },
    Direction.LEFT: {
        "coords": Coord(x=-1, y=0),
        "forbidden": Direction.RIGHT
        },
    Direction.RIGHT: {
        "coords": Coord(x=1, y=0),
        "forbidden": Direction.LEFT
    },
}


class Game:
    def __init__(self, screen: Window):
        self.screen = screen
        self.snake = Snake(screen)
        self.food = Food(screen, self.snake.body)
        self.food_counter: int = 0
        self.score: int = 0

    def make_food(self) -> None:
        """
        Resets the counter to zero and makes new food.
        """
        self.food_counter = 0
        self.food = Food(self.screen, self.snake.body)

    def handle_food(self) -> None:
        """
        Handles automatic food creation (every 10 seconds), as well as eating in
        case the snake touches the food. Score is updated appropriately, too.
        """
        self.food_counter += 1

        if self.food_counter == 100:
            self.make_food()

        if self.snake.is_touching_food(self.food):
            self.snake.eat_food()
            self.score += 1
            self.make_food()

    def set_direction_if_possible(self, direction: Direction) -> None:
        """
        Sets snake direction while making sure it does not go the wrong way.
        """
        if direction == DIRECTIONS[self.snake.direction]["forbidden"]:
            return None
        self.snake.direction = direction

    def restart(self) -> None:
        """
        Restarts the game by putting all vital game parameters to initial state.
        """
        self.snake = Snake(self.screen)
        self.food = Food(self.screen, self.snake.body)
        self.food_counter = 0
        self.score = 0

    async def pause(self) -> None:
        """
        Pauses the gameplay and waits for user input. If the input is key "p",
        it quits waiting and goes back to main game loop.
        """
        while True:
            try:
                user_input = self.screen.getch()
            except curses.error:
                await trio.sleep(0.1)
                continue
            if ord("p") == user_input:
                break


class Snake:
    def __init__(self, screen: Window):
        self.screen = screen
        self.direction = Direction.RIGHT
        self.body = self.init_body()

    def init_body(self) -> Deque[Coord]:  # pylint: disable=no-self-use
        half_width = PLAYGROUND_WIDTH // 4
        half_height = PLAYGROUND_HEIGHT // 2  
        return collections.deque(
            [Coord(y=half_height, x=half_width + i) for i in range(-3, 4)],
            maxlen=7,
        )

    def move(self) -> None:
        """
        Moves the snake one step towards a certain direction,
        while making sure it doesn't crash with itself or the walls.
        """
        next_step = self.get_next_step()
        if self.is_about_to_collide(next_step):
            raise CollisionError
        self.body.append(next_step)

    def eat_food(self) -> None:
        """
        Eats food on the way and grows snake body by a piece.
        """
        current_max_length: Optional[int] = self.body.maxlen
        assert current_max_length is not None
        self.body = collections.deque(self.body, maxlen=current_max_length + 1)
        self.body.insert(
            0, self.body[0] + DIRECTIONS[self.direction]["coords"]
        )

    def is_about_to_collide(self, next_step: Coord) -> bool:
        """
        Returns true if snake is about to collide with itself or the walls.
        """
        return any([
            next_step in self.body,
            self.body[-1].y in {0, PLAYGROUND_HEIGHT - 1},
            self.body[-1].x in {0, PLAYGROUND_WIDTH // 2 - 1},
        ])

    def is_touching_food(self, food) -> bool:
        """
        Returns true if snake's head touches food in any way.
        """
        return self.body[-1] == food.coord

    def get_next_step(self) -> Coord:
        """
        Gets next step based on current direction in [Y, X] form.
        """
        return self.body[-1] + DIRECTIONS[self.direction]["coords"]


class Food:
    def __init__(self, screen: Window, body: Deque[Coord]):
        self.screen = screen
        while True:
            y = random.randint(1, PLAYGROUND_HEIGHT - 2)
            x = random.randint(1, PLAYGROUND_WIDTH // 2 - 2)
            self.coord = Coord(y, x)
            if not self.is_overlapping_snake(body):
                break

    def is_overlapping_snake(self, body: Deque[Coord]) -> bool:
        """
        Returns true if food is about to be drawn on top of snake.
        """
        return self.coord in body


class CollisionError(Exception):
    pass
