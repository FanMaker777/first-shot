import pyxel

from firstshot.constants import CLEAR_COLOR
from firstshot.entities import Bullet, Blast
from firstshot.entities.enemies import Enemy


# ステージ2のボスクラス
class StageTwoBossLeft(Enemy):
    """ステージ2で登場する左側のボス。"""

    # 敵を初期化してゲームに登録する
    def __init__(self, game, level, x, y):
        """ボスを初期化してゲームに登録する。"""

        super().__init__(game, level, x, y)
        self.level = 50  # 強さ
        self.armor = 50  # 装甲
        self.hit_area = (0, 0, 63, 63)

    # 敵にダメージを与える
    def add_damage(self):
        """ボスがダメージを受けた際の処理。"""
        if self.armor > 0:  # 装甲が残っている時
            self.armor -= 1

            return

        # 爆発エフェクトを生成する
        Blast(self.game, self.x + 4, self.y + 4)

        # 爆発音を再生する
        self.game.sound_manager.se_blast.play()

        # 敵をリストから削除する
        if self in self.game.enemy_state.enemies:  # 敵リストに登録されている時
            self.game.enemy_state.enemies.remove(self)

        # スコアを加算する
        self.game.game_data.score += self.level * 10
        # 経験値を加算する
        self.game.player_state.exp += self.level * 1

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
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x +32, self.y + 32, i * 45 + 22, 5)

        # 一定時間毎に自機の方向に向けて弾を発射する
        if self.life_time % 50 == 0:
            player_angle = self.calc_player_angle(self.x + 32,self.y + 32)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, player_angle, 2)


    # 敵を描画する
    def draw(self):
        """ボスを描画する。"""
        pyxel.blt(self.x, self.y, self.game.boss_state.image, 0, 24, 64, 80, CLEAR_COLOR)
