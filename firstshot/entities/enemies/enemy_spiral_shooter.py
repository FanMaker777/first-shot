"""
ステージ3用の敵キャラクター: SpiralShooter の定義

螺旋状の弾幕を放つ移動型敵を実装するモジュール。
"""
import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


class SpiralShooter(Enemy):
    """螺旋状に弾を放つステージ3用の雑魚敵クラス。"""

    def update(self):
        """敵の挙動を更新する。"""
        # 生存時間を増加させる
        self.add_life_time()

        # 徐々に画面下へ移動する
        self.y += 0.5

        # 5フレーム毎に弾を回転させながら発射
        if self.life_time % 5 == 0:
            angle = pyxel.radians(self.life_time * 10 % 360)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 4, self.y + 4, angle, 2)

        # 画面外に出たら削除
        self.delete_out_enemy()

    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 40, 20, 12, 12, COLOR_BLACK)

