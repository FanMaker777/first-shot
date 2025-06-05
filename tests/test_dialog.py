import sys
import types
import pyxel
from tests.helpers import DummyGame
from firstshot.logic.dialog import display_exit_dialog


def test_display_exit_dialog_yes(monkeypatch):
    game = DummyGame()
    quit_called = {}
    monkeypatch.setattr(pyxel, "quit", lambda: quit_called.setdefault("q", True))

    class DummyBox:
        def askyesno(self, title=None, message=None):
            return True

    class DummyTk:
        def withdraw(self):
            pass

        def destroy(self):
            pass

    tk_module = types.ModuleType("tkinter")
    tk_module.Tk = lambda: DummyTk()
    mb_module = types.ModuleType("tkinter.messagebox")
    mb_module.askyesno = DummyBox().askyesno
    monkeypatch.setitem(sys.modules, "tkinter", tk_module)
    monkeypatch.setitem(sys.modules, "tkinter.messagebox", mb_module)
    display_exit_dialog(game)
    assert quit_called


def test_display_exit_dialog_no(monkeypatch):
    game = DummyGame()
    game.game_data.is_exit_mode = True
    monkeypatch.setattr(pyxel, "quit", lambda: None)

    class DummyBox:
        def askyesno(self, title=None, message=None):
            return False

    class DummyTk:
        def withdraw(self):
            pass

        def destroy(self):
            pass

    tk_module = types.ModuleType("tkinter")
    tk_module.Tk = lambda: DummyTk()
    mb_module = types.ModuleType("tkinter.messagebox")
    mb_module.askyesno = DummyBox().askyesno
    monkeypatch.setitem(sys.modules, "tkinter", tk_module)
    monkeypatch.setitem(sys.modules, "tkinter.messagebox", mb_module)
    display_exit_dialog(game)
    assert game.game_data.is_exit_mode is False

