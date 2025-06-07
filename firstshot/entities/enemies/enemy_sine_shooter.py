"""
ステージ3用の敵キャラクター: SineShooter の定義

正弦波を描く軌道で移動しながら弾を撃つ敵を実装するモジュール。
"""
import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


class SineShooter(Enemy):
    """正弦波運動を行う小型敵。"""

    def __init__(self, game, score, exp, armor, x, y, hit_area_x, hit_area_y):
        """基底クラスの初期化に加えて初期位置を記憶する。"""
        super().__init__(game, score, exp, armor, x, y, hit_area_x, hit_area_y)
        self.base_x = x

    def update(self):
        """敵の挙動を更新する。"""
        self.add_life_time()

        # 正弦波に沿って左右へ移動する
        self.x = self.base_x + pyxel.sin(self.life_time * 0.1) * 20
        self.y += 0.8

        # 一定間隔でプレイヤーを狙って弾を発射する
        if self.life_time % 40 == 0:
            angle = self.calc_player_angle(self.x, self.y)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, angle, 2)

        self.delete_out_enemy()

    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 52, 20, 12, 12, COLOR_BLACK)

