# ミサイルクラス
import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet


class Missile(Bullet):

    # ミサイルを描画する
    def draw(self):
        """ミサイルを描画する。"""
        pyxel.blt(self.x, self.y, self.game.special_bullet_image, 7, 2, 12, 26, COLOR_BLACK)