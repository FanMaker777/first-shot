"""
ステージ3用ボスキャラクターの定義。

複数の攻撃パターンを組み合わせた大型の敵を表す。
"""
import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


class StageThreeBoss(Enemy):
    """ステージ3で登場するボスキャラクター。"""

    def add_damage(self):
        """ボスがダメージを受けた際の処理。"""
        super().add_damage()
        # ボスが破壊されたらフラグを立てる
        if self not in self.game.enemy_state.enemies:
            self.game.boss_state.destroyed = True

    def update(self):
        """ボスの挙動を更新する。"""
        self.add_life_time()

        # 画面上部まで移動する
        if self.y < 16:
            self.y += 0.5

        # 定期的に全方向弾
        if self.life_time % 45 == 0:
            for i in range(12):
                Bullet(
                    self.game,
                    Bullet.SIDE_ENEMY,
                    self.x + 32,
                    self.y + 32,
                    pyxel.radians(i * 30),
                    3,
                )

        # プレイヤー狙いの高速弾
        if self.life_time % 90 == 0:
            angle = self.calc_player_angle(self.x + 32, self.y + 32)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, angle, 5)

    def draw(self):
        """ボスを描画する。"""
        pyxel.blt(self.x, self.y, self.game.boss_state.image, 0, 0, 64, 64, COLOR_BLACK)

