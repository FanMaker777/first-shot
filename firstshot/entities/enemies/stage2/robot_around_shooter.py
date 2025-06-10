import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


# 敵クラス
class RobotAroundShooter(Enemy):
    """複数方向に弾を放つロボット型の敵。"""

    # 敵を更新する
    def update(self):
        """敵の挙動を更新する。"""
        # 生存時間をカウントする
        self.add_life_time()

        # 画面上部まで移動させる
        if self.y < 30:
            self.y += 1.0

        # 一定時間毎に6方向に弾を発射する
        if self.life_time % 30 == 0:
            for i in range(6):
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, i * 45 + 22, 3)

        # 一定時間毎に6方向に弾を発射する
        if self.life_time % 90 == 0:
            for i in range(8):
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, i * 45 + 22, 3)

    # 敵を描画する
    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 5, 20, 15, 20, COLOR_BLACK)
