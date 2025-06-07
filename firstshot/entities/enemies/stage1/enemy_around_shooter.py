import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


# 敵クラス
class AroundShooter(Enemy):
    """四方向へ弾を放つ敵キャラクター。"""

    # 敵を更新する
    def update(self):
        """敵の挙動を更新する。"""
        # 生存時間をカウントする
        self.add_life_time()

        # 画面上部まで移動させる
        if self.y < 30:
            self.y += 1.0

        # 一定時間毎に４方向に弾を発射する
        if self.life_time % 40 == 0:
            for i in range(4):
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, i * 45 + 22, 2)

    # 敵を描画する
    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 26, 18, 12, 12, COLOR_BLACK)
