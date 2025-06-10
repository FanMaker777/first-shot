import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy

class WaveShooter(Enemy):
    """左右に揺れながら前進し、一定間隔で弾を撃つ敵。"""

    def update(self):
        """敵の挙動を更新する。"""
        # 生存時間をカウントする
        self.add_life_time()

        # 画面上部まで移動させる
        if self.y < 30:
            self.y += 1.0

        if self.life_time % 90 == 0:
            # プレイヤーに向けた角度を計算
            player_angle = self.calc_player_angle(self.x, self.y)

            Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, player_angle, 3)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, player_angle + 15, 3)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, player_angle - 15, 3)

        # 画面外にでた敵を削除する
        self.delete_out_enemy()

    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 0, 40, 24, 24, COLOR_BLACK)
