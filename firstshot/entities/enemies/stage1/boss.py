import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities.bullets import Bullet
from firstshot.entities.enemies import Enemy


# ステージ1のボスクラス
class StageOneBoss(Enemy):
    """ステージ1のボスキャラクター。"""

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
        if self.life_time % 30 == 0:
            for i in range(8):
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x +32, self.y + 32, i * 45 + 22, 4)

        # 一定時間毎に自機の方向に向けて弾を発射する
        if self.life_time % 50 == 0:
            player_angle = self.calc_player_angle(self.x + 32,self.y + 32)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, player_angle, 2)

        # 一定時間毎に自機の方向に向けて弾を発射する
        if self.life_time % 200 == 0 or self.life_time % 202 == 0 or self.life_time % 204 == 0:
                player_angle = self.calc_player_angle(self.x + 32,self.y + 32)
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, player_angle, 5)


    # 敵を描画する
    def draw(self):
        """ボスを描画する。"""
        pyxel.blt(self.x, self.y, self.game.boss_state.image, 0, 0, 64, 64, COLOR_BLACK)
