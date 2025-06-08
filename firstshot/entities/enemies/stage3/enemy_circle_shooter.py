import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


class CircleShooter(Enemy):
    """円を描くように移動しつつ弾をばらまく敵。"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.angle = 0.0

    def update(self):
        """敵の挙動を更新する。"""
        self.add_life_time()
        self.angle += 0.1
        self.x += pyxel.cos(self.angle) * 1.5
        self.y += pyxel.sin(self.angle) * 1.5 + 0.5
        if self.life_time % 50 == 0:
            for i in range(6):
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, i * 60, 2)
        self.delete_out_enemy()

    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 26, 18, 12, 12, COLOR_BLACK)
