# ミサイルクラス
import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities.bullets import Bullet


class EnemyMissile(Bullet):

    def draw(self):
        """ミサイルを描画する。"""
        pyxel.blt(self.x, self.y, self.game.special_bullet_image, 7, 2, -12, -26, COLOR_BLACK)