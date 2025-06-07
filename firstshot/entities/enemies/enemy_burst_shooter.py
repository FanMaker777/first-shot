"""
ステージ3用の敵キャラクター: BurstShooter の定義

停止と連射を繰り返す特徴を持つ敵を実装するモジュール。
"""
import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


class BurstShooter(Enemy):
    """一定間隔で多方向へ弾を放つ敵。"""

    def update(self):
        """敵の挙動を更新する。"""
        self.add_life_time()

        # 画面上部へ到達するまでは前進
        if self.y < 40:
            self.y += 1.0
        else:
            # 停止しつつ定期的に弾を連射する
            if self.life_time % 60 == 0:
                for i in range(8):
                    Bullet(
                        self.game,
                        Bullet.SIDE_ENEMY,
                        self.x + 6,
                        self.y + 6,
                        pyxel.radians(i * 45),
                        2,
                    )

        self.delete_out_enemy()

    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 64, 20, 12, 12, COLOR_BLACK)

