import pyxel

from firstshot.entities import Bullet, Blast
from firstshot.entities.enemies import Enemy


# ステージ2のボスクラス
class StageTwoBossRight(Enemy):

    # 敵を初期化してゲームに登録する
    def __init__(self, game, level, x, y):

        super().__init__(game, level, x, y)
        self.level = 50  # 強さ
        self.armor = 50  # 装甲
        self.hit_area = (0, 0, 63, 63)

    # 敵にダメージを与える
    def add_damage(self):
        if self.armor > 0:  # 装甲が残っている時
            self.armor -= 1

            # ダメージ音を再生する
            pyxel.play(2, 1, resume=True)  # チャンネル2で割り込み再生させる
            return

        # 爆発エフェクトを生成する
        Blast(self.game, self.x + 4, self.y + 4)

        # 爆発音を再生する
        pyxel.play(2, 2, resume=True)  # チャンネル2で割り込み再生させる

        # 敵をリストから削除する
        if self in self.game.enemies:  # 敵リストに登録されている時
            self.game.enemies.remove(self)

        # スコアを加算する
        self.game.score += self.level * 10
        # 経験値を加算する
        self.game.player_exp += self.level * 1

        # ボス撃破フラグをTrueにする
        self.game.boss_destroy_flag = True

    # 敵を更新する
    def update(self):
        # 生存時間をカウントする
        self.add_life_time()

        # 画面上部まで移動させる
        if self.y < 20:
            self.y += 1.0

        # 一定時間毎に自機の方向に向けて弾を発射する
        if self.life_time % 30 == 0 or self.life_time % 32 == 0 or self.life_time % 34 == 0:
            player_angle = self.calc_player_angle(self.x + 32,self.y + 32)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, player_angle, 5)

        if self.life_time % 60 == 0 or self.life_time % 62 == 0 or self.life_time % 64 == 0:
            player_angle = self.calc_player_angle(self.x + 32,self.y + 32)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, player_angle, 6)

        if self.life_time % 90 == 0 or self.life_time % 92 == 0 or self.life_time % 94 == 0:
            player_angle = self.calc_player_angle(self.x + 32, self.y + 32)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, player_angle, 7)


    # 敵を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, self.game.boss_image, 64, 24, 60, 80, 188)