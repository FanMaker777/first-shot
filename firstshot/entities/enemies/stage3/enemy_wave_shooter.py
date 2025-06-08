import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


class WaveShooter(Enemy):
    """左右に揺れながら前進し、一定間隔で弾を撃つ敵。"""

    def update(self):
        """敵の挙動を更新する。"""
        self.add_life_time()
        self.y += 1.0
        self.x += pyxel.sin(self.life_time * 0.1) * 2.0
        if self.life_time % 45 == 0:
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, pyxel.atan2(1, 0), 3)
        self.delete_out_enemy()

    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 2, 30, 12, 12, COLOR_BLACK)
