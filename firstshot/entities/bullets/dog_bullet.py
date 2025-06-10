# ドッグ弾クラス
import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities.bullets import Bullet


class DogBullet(Bullet):

    # 弾を初期化してゲームに登録する
    def __init__(self, game, side, x, y, angle, speed):
        """弾を初期化しゲームに登録する。"""
        super().__init__(game, side, x, y, angle, speed)
        # 当たり判定を専用に変更
        self.hit_area = (0, 0, 16, 20)

    def draw(self):
        """ドッグ弾を描画する。"""
        pyxel.blt(self.x, self.y, self.game.special_bullet_image, 3, 98, 16, 20, COLOR_BLACK)