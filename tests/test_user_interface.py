import pytest

from snake import core
from snake import user_interface
from tests.fixtures import fake_curses, fake_stdscr
from tests.util import fake_getch_game_over


def test_ensure_terminal_size(fake_curses, fake_stdscr):
    ui = user_interface.UserInterface(fake_stdscr)
    assert ui.ensure_terminal_size()
    fake_curses.LINES = 10
    fake_curses.COLS = 60
    assert not ui.ensure_terminal_size()


def test_display_score(fake_curses, fake_stdscr):
    ui = user_interface.UserInterface(fake_stdscr)
    ui.display_score("100")
    assert (
        user_interface.PLAYGROUND_HEIGHT - 1,
        2,
        " SCORE: 100 ",
        None,
    ) in fake_stdscr.addstred


def test_game_over_screen_quit(monkeypatch, fake_curses, fake_stdscr):
    monkeypatch.setattr(fake_stdscr, "getch", lambda: 113)
    ui = user_interface.UserInterface(fake_stdscr)
    game = core.Game(fake_stdscr)
    with pytest.raises(SystemExit):
        ui.game_over_screen(game)


def test_game_over_screen_restart(monkeypatch, fake_curses, fake_stdscr):
    ui = user_interface.UserInterface(fake_stdscr)
    monkeypatch.setattr(fake_stdscr, "getch", lambda: 114)
    game = core.Game(fake_stdscr)
    game.score = 100
    ui.game_over_screen(game)
    assert game.score == 0 and game.food_counter == 0 and len(game.snake.body) == 7


def test_game_over_screen_exception(monkeypatch, fake_curses, fake_stdscr):
    ui = user_interface.UserInterface(fake_stdscr)
    monkeypatch.setattr(fake_stdscr, "getch", fake_getch_game_over)
    game = core.Game(fake_stdscr)
    ui.game_over_screen(game)
