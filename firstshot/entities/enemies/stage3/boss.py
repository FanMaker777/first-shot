import math

import pyxel

from firstshot.constants import COLOR_DARK_GREEN
from firstshot.entities.bullets import Bullet
from firstshot.entities.enemies import Enemy


class StageThreeBoss(Enemy):
    """
    ステージ3のボスキャラクターを表すクラス。

    Enemyクラスを継承し、ボス特有の攻撃パターン・行動・描画処理を定義する。
    """

    def add_damage(self, damage):
        """
        ボスがダメージを受けた際の処理。

        ・通常のダメージ処理を実行（親クラスのadd_damage呼び出し）
        ・ボスが敵リストから外れている場合、ボス撃破フラグをON
        """
        super().add_damage(damage)  # 親クラスのダメージ処理を実行

        # ボス自身が敵リストに存在しない場合（撃破直後など）
        if self not in self.game.enemy_state.enemies:
            # ゲーム管理側の「ボス撃破」フラグをTrueに設定
            self.game.boss_state.destroyed = True

    def update(self):
        """
        ボスの挙動・攻撃パターンを毎フレーム更新する。

        - 画面上部に現れるまで徐々に降下
        - 複数のタイミングで多彩な弾幕攻撃を発射
        """
        self.add_life_time()  # 出現後の生存フレーム数をカウント

        # y座標20まで徐々に降下して停止
        if self.y < 20:
            self.y += 1.0

        # 60フレームごとに全方位8方向弾を2箇所から同時発射
        if self.life_time % 60 == 0:
            for i in range(8):
                # 左側：32,32中心
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, i * 45 + 22, 4)
            for i in range(8):
                # 右側：96,32中心
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 96, self.y + 32, i * 45 + 22, 4)

        # 130,140,150,160,170フレーム周期（±ランダム）で狙い撃ち弾5連発
        if (self.life_time % (130 + pyxel.rndi(-5,5)) == 0
                or self.life_time % (140 + pyxel.rndi(-5,5)) == 0
                or self.life_time % (150 + pyxel.rndi(-5, 5)) == 0
                or self.life_time % (160 + pyxel.rndi(-5, 5)) == 0
                or self.life_time % (170 + pyxel.rndi(-5,5)) == 0):

            # プレイヤーへの角度計算
            angle = self.calc_player_angle(self.x + 64, self.y + 64)
            for i in range(5):
                # プレイヤー方向±ランダムで5発
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 64, self.y + 64, angle + pyxel.rndi(-10,10), 1)

        # 300フレームごとに6方向放射点から3WAY弾（左右2点からそれぞれ実行）
        if self.life_time % 300 == 0:
            # 左側：32,32中心
            angle = self.calc_player_angle(self.x + 32, self.y + 32)
            for i in range(6):
                theta = 2 * math.pi * i / 6
                x = 10 * math.cos(theta)  # 半径10の円上に配置
                y = 10 * math.sin(theta)
                # プレイヤー方向へ
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32 + x, self.y + 32 + y, angle, 2)
                # 左右に25度ずらした弾も発射
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32 + x, self.y + 32 + y, angle - 25, 2)
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32 + x, self.y + 32 + y, angle + 25, 2)

            # 右側：96,32中心
            angle = self.calc_player_angle(self.x + 96, self.y + 32)
            for i in range(6):
                theta = 2 * math.pi * i / 6
                x = 10 * math.cos(theta)
                y = 10 * math.sin(theta)
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 96 + x, self.y + 32 + y, angle, 2)
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 96 + x, self.y + 32 + y, angle - 25, 2)
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 96 + x, self.y + 32 + y, angle + 25, 2)

    def draw(self):
        """
        ボスを画面上に描画する。

        - ボス用イメージを現在座標に描画（指定色で透過）
        """
        pyxel.blt(
            self.x, self.y,                         # 描画先座標（左上）
            self.game.boss_state.image,             # ボス用イメージバンク
            0, 0, 128, 128,             # イメージ内の(0,0)から128x128ピクセルを使用
            COLOR_DARK_GREEN                        # この色を透過色として指定
        )
