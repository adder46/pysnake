import pytest
from snake import application
from snake import core
from snake import user_interface
from tests.fixtures import (
    fake_curses,
    fake_stdscr,
)
from tests.util import fake_game_over, fake_getch_app, fake_pause


@pytest.mark.parametrize(
    "attr, value",
    [
        ["LINES", user_interface.PLAYGROUND_HEIGHT - 1],
        ["COLS", user_interface.PLAYGROUND_WIDTH - 1],
    ],
)
async def test_ensuring_terminal_size(
    monkeypatch, fake_curses, fake_stdscr, attr, value
):
    monkeypatch.setattr(fake_curses, attr, value)
    with pytest.raises(AssertionError):
        await application.main(fake_stdscr)


async def test_user_input(monkeypatch, fake_curses, fake_stdscr):
    monkeypatch.setattr(fake_stdscr, "getch", fake_getch_app)
    monkeypatch.setattr(core.Game, "pause", fake_pause)
    with pytest.raises(SystemExit):
        await application.main(fake_stdscr)


async def test_collision(monkeypatch, fake_curses, fake_stdscr):
    monkeypatch.setattr(
        user_interface.UserInterface, "display_game_over_screen", fake_game_over
    )
    with pytest.raises(core.CollisionError):
        await application.main(fake_stdscr)
