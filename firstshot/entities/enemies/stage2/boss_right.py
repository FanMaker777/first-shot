import pyxel

from firstshot.constants import COLOR_GREEN
from firstshot.entities.bullets import Bullet
from firstshot.entities.bullets import EnemyMissile
from firstshot.entities.enemies import Enemy


class StageTwoBossRight(Enemy):
    """ステージ2で登場する右側のボス。"""

    def add_damage(self, damage):
        """ボスがダメージを受けた際の処理。"""
        super().add_damage(damage)

        # 敵リストに登録されていない時
        if not self in self.game.enemy_state.enemies:
            # ボス撃破フラグをTrueにする
            self.game.boss_state.destroyed_stage2_right = True

    def update(self):
        """ボスの挙動を更新する。"""
        # 生存時間をカウントする
        self.add_life_time()

        # 画面上部まで移動させる
        if self.y < 20:
            self.y += 1.0

        # 一定時間毎に自機の方向に向けて弾を発射する
        if self.life_time % 60 == 0 or self.life_time % 62 == 0 or self.life_time % 64 == 0:
            player_angle = self.calc_player_angle(self.x + 32,self.y + 32)
            EnemyMissile(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, player_angle, 3)

        if self.life_time % 120 == 0 or self.life_time % 122 == 0 or self.life_time % 124 == 0:
            player_angle = self.calc_player_angle(self.x + 32, self.y + 32)
            EnemyMissile(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, player_angle, 3)

        if self.life_time % 300 == 0:
            player_angle = self.calc_player_angle(self.x + 32, self.y + 32)
            EnemyMissile(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, player_angle, 6)
            EnemyMissile(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, player_angle - 15, 6)
            EnemyMissile(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, player_angle + 15, 6)


    # 敵を描画する
    def draw(self):
        """ボスを描画する。"""
        pyxel.blt(self.x, self.y, self.game.boss_state.image, 61, 24, 60, 80, COLOR_GREEN)
