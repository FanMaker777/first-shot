import pyxel
import math
from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


class CircleShooter(Enemy):
    """円を描くように移動しつつ弾をばらまく敵。"""

    def update(self):
         # 生存時間をカウントする
        self.add_life_time()

        # 画面上部まで移動させる
        if self.y < 20:
            self.y += 1.0

        if self.life_time % 60 == 0:
            # プレイヤーに向けた角度を計算
            player_angle = self.calc_player_angle(self.x, self.y)

            for i in range(6):
                theta = 2 * math.pi * i / 6
                x = 10 * math.cos(theta)
                y = 10 * math.sin(theta)
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + x, self.y + y, player_angle, 2)

         # 画面外にでた敵を削除する
        self.delete_out_enemy()

    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 24, 16, 24, 24,COLOR_BLACK)
