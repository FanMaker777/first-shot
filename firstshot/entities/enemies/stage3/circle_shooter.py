import math

import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities.bullets import Bullet
from firstshot.entities.enemies import Enemy


class CircleShooter(Enemy):
    """
    円状の弾をばらまく敵キャラクター。
    Enemyクラスを継承し、周期的な弾発射や上昇制御などを実装。
    """

    def update(self):
        """
        毎フレーム呼ばれる敵の挙動更新処理。
        - 画面上部(y=20)までは上昇
        - 60フレームごとに6点円状配置からプレイヤー方向への弾を発射
        - 画面外に出た場合は自身を削除
        """
        self.add_life_time()  # 敵の生存フレーム数をカウント

        # y座標20まで下降し、そこで停止
        if self.y < 20:
            self.y += 1.0

        # 60フレームごとに弾発射処理
        if self.life_time % 60 == 0:
            player_angle = self.calc_player_angle(self.x, self.y)  # プレイヤーへの角度計算

            # 円周上に6点（60度ずつ）配置し、そこからプレイヤー方向へ同時発射
            for i in range(6):
                theta = 2 * math.pi * i / 6  # 0, 60, 120, ... 角度
                x = 10 * math.cos(theta)     # 半径10の円座標
                y = 10 * math.sin(theta)
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + x, self.y + y, player_angle, 2)

        # 画面外（エリア外）に出た場合は自身を削除
        self.delete_out_enemy()

    def draw(self):
        """
        敵キャラクターを画面に描画する。
        - イメージバンク0の(24,16)から24x24ピクセルをself.x,self.yに描画
        - COLOR_BLACKを透過色として利用
        """
        pyxel.blt(self.x, self.y, 0, 24, 16, 24, 24, COLOR_BLACK)  # 引数は改行せず1行
