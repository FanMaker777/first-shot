import pyxel

from firstshot.constants import PLAYER_BULLET_ANGLE_UP
from firstshot.entities.bullets import Missile, Bullet, DogBullet

def skill(game, x, y):
    if game.player_state.skill_cool_time > 0:
        # ドッグ弾を追加発射
        for i in range(5):
            DogBullet(game, Bullet.SIDE_PLAYER, x, y, pyxel.rndi(-25, -155), 7)