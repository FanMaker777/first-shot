import pyxel

from firstshot.constants import CLEAR_COLOR

from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


# 敵クラス
class PlayerShooter(Enemy):

    # 敵を更新する
    def update(self):
        # 生存時間をカウントする
        self.add_life_time()

        # 画面上部まで移動させる
        if self.y < 20:
            self.y += 1.0

        # 一定時間毎に自機の方向に向けて弾を発射する
        if self.life_time % 50 == 0:
            player_angle = self.calc_player_angle(self.x,self.y)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, player_angle, 2)

    # 敵を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 15, 52, 12, 12, CLEAR_COLOR)
