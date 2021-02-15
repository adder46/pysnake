import time
from snake import core
from tests.fixtures import FakeCurses


def fake_game_over(*args):
    raise core.CollisionError


getch_results_app = iter(
    [
        "raise",
        FakeCurses.KEY_UP,
        FakeCurses.KEY_DOWN,
        FakeCurses.KEY_LEFT,
        FakeCurses.KEY_RIGHT,
        "raise",
        "p",
        "q",
    ]
)


def fake_getch_app():
    result = next(getch_results_app)
    if result == "raise":
        raise FakeCurses.error
    elif result == FakeCurses.KEY_UP:
        return 259
    elif result == FakeCurses.KEY_DOWN:
        return 258
    elif result == FakeCurses.KEY_LEFT:
        return 260
    elif result == FakeCurses.KEY_RIGHT:
        return 261
    elif result == "p":
        return ord("p")
    elif result == "q":
        return ord("q")


getch_results_pause = iter(["raise", "p"])


def fake_getch_pause():
    result = next(getch_results_pause)
    if result == "raise":
        raise FakeCurses.error
    elif result == "p":
        return ord("p")


def fake_pause(*args):
    time.sleep(0.1)


getch_results_game_over = iter(["raise", "r"])


def fake_getch_game_over():
    result = next(getch_results_game_over)
    if result == "raise":
        raise FakeCurses.error
    elif result == "r":
        return ord("r")
