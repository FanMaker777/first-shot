import pyxel

from firstshot.constants import COLOR_GREEN
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


# ステージ2のボスクラス
class StageTwoBossLeft(Enemy):
    """ステージ2で登場する左側のボス。"""

    # 敵にダメージを与える
    def add_damage(self):
        """ボスがダメージを受けた際の処理。"""
        super().add_damage()

        # 敵リストに登録されていない時
        if not self in self.game.enemy_state.enemies:
            # ボス撃破フラグをTrueにする
            self.game.boss_state.destroyed = True

    # 敵を更新する
    def update(self):
        """ボスの挙動を更新する。"""
        # 生存時間をカウントする
        self.add_life_time()

        # 画面上部まで移動させる
        if self.y < 20:
            self.y += 1.0

        # 一定時間毎に４方向に弾を発射する
        if self.life_time % 30 == 0 or self.life_time % 35 == 0 or self.life_time % 40 == 0:
            for i in range(8):
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x +32, self.y + 32, i * 45 + 22, 3)

        # 一定時間毎に４方向に弾を発射する
        if self.life_time % 60 == 0 or self.life_time % 65 == 0 or self.life_time % 70 == 0:
            for i in range(8):
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, i * 45 + 22, 3)


    # 敵を描画する
    def draw(self):
        """ボスを描画する。"""
        pyxel.blt(self.x, self.y, self.game.boss_state.image, 0, 24, 60, 80, COLOR_GREEN)
