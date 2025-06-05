import types
import pytest
import pyxel

from firstshot.entities import Blast, Bullet, Player
from firstshot.entities.enemies import (
    Enemy,
    Zigzag,
    AroundShooter,
    PlayerShooter,
    RobotAroundShooter,
    RobotPlayerShooter,
    RobotFollow,
)
from firstshot.entities.enemies.enemy_stage1_boss import StageOneBoss
from firstshot.entities.enemies.enemy_stage2_boss_left import StageTwoBossLeft
from firstshot.entities.enemies.enemy_stage2_boss_right import StageTwoBossRight
from firstshot.constants import SCENE_GAMEOVER, SCENE_PLAY_STAGE_ONE
from tests.helpers import DummyGame


def reset_inputs():
    for key in [pyxel.KEY_LEFT, pyxel.KEY_RIGHT, pyxel.KEY_UP, pyxel.KEY_DOWN, pyxel.KEY_SPACE, pyxel.KEY_RETURN, pyxel.KEY_E]:
        pyxel.set_btn(key, False)
        pyxel.set_btnp(key, False)


def test_blast_update_removes_when_radius_exceeds():
    game = DummyGame()
    blast = Blast(game, 0, 0)
    blast.radius = blast.END_RADIUS
    blast.update()
    assert blast not in game.enemy_state.blasts


def test_bullet_add_damage_removes_from_list():
    game = DummyGame()
    b = Bullet(game, Bullet.SIDE_PLAYER, 0, 0, 0, 0)
    assert b in game.player_state.bullets
    b.add_damage()
    assert b not in game.player_state.bullets


def test_bullet_update_moves_and_removes_offscreen():
    game = DummyGame()
    b = Bullet(game, Bullet.SIDE_PLAYER, 0, 0, 0, 1)
    b.update()
    assert b.x != 0
    b.x = pyxel.width + 10
    b.update()
    assert b not in game.player_state.bullets


def test_player_add_damage_triggers_gameover():
    game = DummyGame()
    p = Player(game, 0, 0)
    p.add_damage()
    assert game.player_state.instance is None
    assert game.changed_scene_to == SCENE_GAMEOVER
    assert len(game.enemy_state.blasts) == 1


def test_player_update_level_up_and_shoot():
    game = DummyGame()
    p = Player(game, 0, 0)
    game.player_state.exp = 8
    pyxel.set_btn(pyxel.KEY_SPACE, True)
    p.update()
    pyxel.set_btn(pyxel.KEY_SPACE, False)
    assert game.player_state.lv == 2
    assert len(game.player_state.bullets) == 1
    assert p.shot_timer == p.shot_interval


def test_enemy_add_damage_and_destroy():
    game = DummyGame()
    game.game_data.scene_name = SCENE_PLAY_STAGE_ONE
    e = Enemy(game, 2, 0, 0)
    e.add_damage()
    assert e.armor == 0 and e in game.enemy_state.enemies
    e.add_damage()
    assert e not in game.enemy_state.enemies
    assert len(game.enemy_state.blasts) == 1
    assert game.game_data.score > 0


def test_enemy_calc_player_angle_and_delete_out():
    game = DummyGame()
    e = Enemy(game, 1, 0, pyxel.height + 1)
    angle_no_player = e.calc_player_angle(0, 0)
    assert angle_no_player == 90
    Player(game, 10, 0)
    angle_with_player = e.calc_player_angle(0, 0)
    assert angle_with_player == pyxel.atan2(-0, 10)
    e.delete_out_enemy()
    assert e not in game.enemy_state.enemies


def test_zigzag_update_moves():
    game = DummyGame()
    z = Zigzag(game, 1, 0, 0)
    z.update()
    assert z.y == 1
    assert z.x != 0


def test_enemy_shooters_spawn_bullets():
    game = DummyGame()
    a = AroundShooter(game, 1, 0, 0)
    a.life_time = 39
    a.update()
    assert len(game.enemy_state.bullets) == 4

    ps = PlayerShooter(game, 1, 0, 0)
    ps.life_time = 49
    ps.update()
    assert len(game.enemy_state.bullets) == 5

    ra = RobotAroundShooter(game, 1, 0, 0)
    ra.life_time = 39
    ra.update()
    assert len(game.enemy_state.bullets) == 11

    rp = RobotPlayerShooter(game, 1, 0, 0)
    rp.life_time = 29
    rp.update()
    assert len(game.enemy_state.bullets) == 12


def test_robot_follow_chases_player():
    game = DummyGame()
    Player(game, 10, 10)
    rf = RobotFollow(game, 1, 0, 0)
    rf.update()
    assert rf.x == 1 and rf.y == 1


def test_bosses_update_and_damage():
    game = DummyGame()
    boss1 = StageOneBoss(game, 50, 0, 0)
    boss1.life_time = 29
    boss1.update()
    assert len(game.enemy_state.bullets) == 8
    boss1.armor = 1
    boss1.add_damage()
    boss1.add_damage()
    assert game.boss_state.destroyed

    game.enemy_state.bullets.clear()
    game.boss_state.destroyed = False
    left = StageTwoBossLeft(game, 50, 0, 0)
    left.life_time = 29
    left.update()
    assert len(game.enemy_state.bullets) >= 8
    left.armor = 1
    left.add_damage()
    left.add_damage()
    assert game.boss_state.destroyed

    game.enemy_state.bullets.clear()
    game.boss_state.destroyed = False
    right = StageTwoBossRight(game, 50, 0, 0)
    right.life_time = 29
    right.update()
    assert len(game.enemy_state.bullets) >= 1
    right.armor = 1
    right.add_damage()
    right.add_damage()
    assert game.boss_state.destroyed

