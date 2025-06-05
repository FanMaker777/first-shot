import types, pygame
pygame.mixer = types.SimpleNamespace(music=types.SimpleNamespace(stop=lambda *a, **k: None, load=lambda *a, **k: None, set_volume=lambda *a, **k: None, play=lambda *a, **k: None))
import pyxel
from tests.helpers import DummyGame
from firstshot.constants import (
    SCENE_PLAY_STAGE_TWO,
    SCENE_PLAY_STAGE_ONE,
    SCENE_SELECT_PILOT,
    SCENE_TITLE,
    GAMEOVER_DISPLAY_TIME,
)
from firstshot.scenes.scenes_play_stage import PlayScene, StageOneScene, StageTwoScene
from firstshot.scenes.select_pilot_scene import SelectPilotScene
from firstshot.scenes.title_scene import TitleScene
from firstshot.scenes.gameover_scene import GameoverScene
from firstshot.scenes.background_scene import Background


def test_play_scene_update_increments_time():
    game = DummyGame()
    scene = PlayScene(game)
    scene.start()
    scene.update()
    assert game.game_data.play_time == 1


def test_stage_one_scene_boss_transition():
    game = DummyGame()
    scene = StageOneScene(game)
    scene.start()
    game.boss_state.destroyed = True
    scene.update()
    assert game.changed_scene_to == SCENE_PLAY_STAGE_TWO


def test_stage_one_scene_activate_boss():
    game = DummyGame()
    scene = StageOneScene(game)
    scene.start()
    game.game_data.play_time = 180
    scene.update()
    assert game.boss_state.active


def test_stage_two_scene_activate_boss():
    game = DummyGame()
    scene = StageTwoScene(game)
    scene.start()
    game.game_data.play_time = 300
    scene.update()
    assert game.boss_state.active


def test_select_pilot_scene_input_and_start_game():
    game = DummyGame()
    scene = SelectPilotScene(game)
    scene.start()
    pyxel.set_btnp(pyxel.KEY_RIGHT, True)
    scene.update()
    assert scene.pilot_kind == 1
    pyxel.set_btnp(pyxel.KEY_RETURN, True)
    scene.update()
    assert game.changed_scene_to == SCENE_PLAY_STAGE_ONE
    assert game.player_state.pilot_kind == 1


def test_title_scene_start_game():
    game = DummyGame()
    scene = TitleScene(game)
    pyxel.set_btnp(pyxel.KEY_RETURN, True)
    scene.update()
    assert game.changed_scene_to == SCENE_SELECT_PILOT


def test_gameover_scene_timer_and_transition():
    game = DummyGame()
    scene = GameoverScene(game)
    scene.start()
    assert game.display_timer == GAMEOVER_DISPLAY_TIME
    scene.update()
    assert game.display_timer == GAMEOVER_DISPLAY_TIME - 1
    game.display_timer = 0
    scene.update()
    assert game.changed_scene_to == SCENE_TITLE


def test_background_update_loops():
    game = DummyGame()
    bg = Background(game)
    x, y, vy = bg.stars[0]
    bg.stars[0] = (x, pyxel.height + 1, vy)
    bg.update()
    assert bg.stars[0][1] < pyxel.height
