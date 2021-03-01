import pytest
from snake import application
from snake import core
from snake import user_interface
from snake.user_interface import PLAYGROUND_HEIGHT, PLAYGROUND_WIDTH


class FakeCurses:
    class error(Exception):
        pass

    LINES = PLAYGROUND_HEIGHT
    COLS = PLAYGROUND_WIDTH
    COLOR_WHITE = None
    COLOR_RED = None
    A_BOLD = None
    KEY_UP = 259
    KEY_DOWN = 258
    KEY_LEFT = 260
    KEY_RIGHT = 261

    def color_pair(self, *args):
        pass

    def curs_set(self, *args):
        pass

    def init_pair(self, *args):
        pass

    def initscr(self, *args):
        return FakeStdscr()

    def wrapper(self, *args):
        return FakeStdscr()

    def newwin(self, *args):
        return FakeStdscr()


class FakeStdscr:
    def __init__(self):
        self.addstred = []

    def addstr(self, *args):
        self.addstred.append(args)

    def box(self, *args):
        pass

    def timeout(self, *args):
        pass

    def subwin(self, *args):
        return FakeStdscr()

    def clear(self):
        pass

    def erase(self):
        pass

    def refresh(self):
        pass

    def getch(self):
        pass

    def nodelay(self, *args):
        pass

    def keypad(self, *args):
        pass


@pytest.fixture
def fake_curses(monkeypatch):
    fc = FakeCurses()
    monkeypatch.setattr(application, "curses", fc)
    monkeypatch.setattr(user_interface, "curses", fc)
    return fc


@pytest.fixture
def fake_stdscr():
    return FakeStdscr()
