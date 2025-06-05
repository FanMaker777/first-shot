import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from firstshot.entities.laser import Laser

class DummyEnemyState:
    def __init__(self):
        self.enemies = []
        self.bullets = []
        self.blasts = []

class DummyGame:
    def __init__(self):
        self.enemy_state = DummyEnemyState()

def test_laser_removed_after_duration():
    game = DummyGame()
    laser = Laser(game, 0, 0, 90, 10, 2)
    assert laser in game.enemy_state.bullets
    laser.update()
    assert laser in game.enemy_state.bullets
    laser.update()
    assert laser not in game.enemy_state.bullets


def test_laser_stores_angle():
    game = DummyGame()
    laser = Laser(game, 0, 0, 45, 10, 1)
    assert laser.angle == 45
