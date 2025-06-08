import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


class ChargeShooter(Enemy):
    """高速で突進し停止後にプレイヤーを狙う敵。"""

    def update(self):
        """敵の挙動を更新する。"""
        self.add_life_time()
        if self.life_time < 20:
            self.y += 2.5
        else:
            self.y += 0.5
            if self.life_time % 40 == 0:
                angle = self.calc_player_angle(self.x, self.y)
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, angle, 4)
        self.delete_out_enemy()

    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 0, 16, 24, 24,COLOR_BLACK)
