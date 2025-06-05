import types
import pyxel
from tests.helpers import DummyGame
from firstshot.game_data import GameData
from firstshot.constants import SCENE_SELECT_PILOT
from firstshot.logic.dialog import display_exit_dialog


class SceneStub:
    def __init__(self):
        self.started = False
        self.updated = False
    def start(self):
        self.started = True
    def update(self):
        self.updated = True
    def draw(self):
        pass


class GameForTest(DummyGame):
    def __init__(self):
        super().__init__()
        self.scenes = {"a": SceneStub(), "b": SceneStub()}
        self.game_data.scene_name = "a"
        self.game_data.background = types.SimpleNamespace(update=lambda: None)

    def change_scene(self, scene_name):
        self.changed_scene_to = scene_name
        self.game_data.scene_name = scene_name
        self.scenes[scene_name].start()

    def update(self):
        if not self.game_data.is_exit_mode and pyxel.btnp(pyxel.KEY_E):
            self.game_data.is_exit_mode = True
            display_exit_dialog(self)
            return
        if self.game_data.is_exit_mode:
            return
        self.scenes[self.game_data.scene_name].update()
        if self.game_data.scene_name != SCENE_SELECT_PILOT:
            self.game_data.background.update()


def test_change_scene_calls_start():
    game = GameForTest()
    game.change_scene("b")
    assert game.game_data.scene_name == "b"
    assert game.scenes["b"].started


def test_game_update_handles_exit():
    game = GameForTest()
    pyxel.set_btnp(pyxel.KEY_E, True)
    called = {}
    def fake_dialog(g):
        called['x'] = True
    display_exit_dialog_orig = display_exit_dialog
    try:
        globals()['display_exit_dialog'] = fake_dialog
        game.update()
        assert called
        assert game.game_data.is_exit_mode
    finally:
        globals()['display_exit_dialog'] = display_exit_dialog_orig
