import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy

class TridentShooter(Enemy):
    """
    自機狙いで3方向（トライデント状）に弾を撃つ敵キャラクター。

    Enemyクラスを継承し、移動と三連射パターンを実装する。
    """

    def update(self):
        """
        毎フレーム呼ばれる敵の挙動更新処理。

        - 画面上部(y=30)までは上昇
        - 90フレームごとにプレイヤー狙い三連射（中心+左右±15度）
        - 画面外に出た場合は自身を削除
        """
        self.add_life_time()  # 敵の生存フレーム数をカウント

        # y座標30まで上昇し、そこで停止
        if self.y < 30:
            self.y += 1.0

        # 90フレームごとに自機狙い三連弾を発射
        if self.life_time % 90 == 0:
            player_angle = self.calc_player_angle(self.x, self.y)  # プレイヤーへの角度計算

            Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, player_angle, 3)         # 真ん中
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, player_angle + 15, 3)    # 右（+15度）
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x, self.y, player_angle - 15, 3)    # 左（-15度）

        # 画面外（エリア外）に出た場合は自身を削除
        self.delete_out_enemy()

    def draw(self):
        """
        敵キャラクターを画面に描画する。

        - イメージバンク0の(0,40)から24x24ピクセルをself.x,self.yに描画
        - COLOR_BLACKを透過色として利用
        """
        pyxel.blt(self.x, self.y, 0, 0, 40, 24, 24, COLOR_BLACK)
