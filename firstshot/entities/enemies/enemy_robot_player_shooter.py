import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


# 敵クラス
class RobotPlayerShooter(Enemy):
    """プレイヤーを狙うロボット型の敵。"""

    # 敵を更新する
    def update(self):
        """敵の挙動を更新する。"""
        # 生存時間をカウントする
        self.add_life_time()

        # 画面上部まで移動させる
        if self.y < 20:
            self.y += 1.0

        # 一定時間毎に自機の方向に向けて弾を発射する
        if self.life_time % 30 == 0:
            player_angle = self.calc_player_angle(self.x,self.y)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, player_angle, 3)

    # 敵を描画する
    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 2, 42, 18, 18, COLOR_BLACK)
