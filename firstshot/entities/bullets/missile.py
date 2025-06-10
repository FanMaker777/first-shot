# ミサイルクラス
import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities.bullets import Bullet


class Missile(Bullet):

    # 弾を初期化してゲームに登録する
    def __init__(self, game, side, x, y, angle, speed):
        """弾を初期化しゲームに登録する。"""
        super().__init__(game, side, x, y, angle, speed)
        # ダメージと当たり判定をミサイル専用に変更
        self.damage = 5
        self.hit_area = (0, 0, 12, 26)

    def draw(self):
        """ミサイルを描画する。"""
        pyxel.blt(self.x, self.y, self.game.special_bullet_image, 7, 2, 12, 26, COLOR_BLACK)