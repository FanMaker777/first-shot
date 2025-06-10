import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


class ChargeShooter(Enemy):
    """高速で突進し停止後にプレイヤーを狙う敵。"""

    def update(self):
        """敵の挙動を更新する。"""
        # 生存時間をカウントする
        self.add_life_time()

        if self.life_time < 30:
            self.y += 2.5
        else:
            self.y += 0.5
            if self.life_time % 10 == 0:
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, pyxel.rndi(-360,360), 2)

        # 画面外にでた敵を削除する
        self.delete_out_enemy()

    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 0, 16, 24, 24,COLOR_BLACK)
