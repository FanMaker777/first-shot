import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities.enemies import Enemy


# 敵クラス
class Zigzag(Enemy):
    """左右にジグザグ移動する敵キャラクター。"""

    # 敵を更新する
    def update(self):
        """敵の挙動を更新する。"""
        # 生存時間をカウントする
        self.add_life_time()

        # 前方に移動させる
        self.y += 1

        # 経過時間に応じて左右に移動する
        if self.life_time // 30 % 2 == 0:
            self.x += 1.2
        else:
            self.x -= 1.2

        # 画面外にでた敵を削除する
        self.delete_out_enemy()

    # 敵を描画する
    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 2, 30, 12, 12, COLOR_BLACK)
