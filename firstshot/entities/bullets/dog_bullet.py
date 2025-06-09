# ドッグ弾クラス
import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet


class DogBullet(Bullet):

    def draw(self):
        """ドッグ弾を描画する。"""
        pyxel.blt(self.x, self.y, self.game.special_bullet_image, 3, 98, 16, 20, COLOR_BLACK)