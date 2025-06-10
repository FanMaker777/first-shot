import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities.bullets import Bullet
from firstshot.entities.enemies import Enemy


class ChargeShooter(Enemy):
    """
    高速で突進し、停止後にプレイヤーを狙う弾を撃つ敵キャラクター。
    Enemyクラスを継承し、突進後の挙動や射撃パターンを実装する。
    """

    def update(self):
        """
        毎フレーム呼ばれる敵の挙動更新処理。
        ・出現後30フレームは高速突進
        ・以降は減速し、一定間隔でランダム方向に弾を発射
        ・画面外に出たら自身を削除
        """
        self.add_life_time()  # 敵の生存フレーム数をインクリメント

        if self.life_time < 30:
            # 出現から30フレーム未満は高速で下に移動（突進）
            self.y += 2.5
        else:
            # 31フレーム目以降は減速
            self.y += 0.5
            # 10フレームごとにランダム方向へ弾を1発発射
            if self.life_time % 10 == 0:
                Bullet(
                    self.game,
                    Bullet.SIDE_ENEMY,
                    self.x,
                    self.y,
                    pyxel.rndi(-360, 360),  # -360～+360度のランダム角度
                    2                       # 弾速
                )

        # 画面外に出た場合、自身を削除する
        self.delete_out_enemy()

    def draw(self):
        """
        敵キャラクターを画面に描画する。
        - 指定座標(self.x, self.y)にイメージバンク0の(0,16)から24x24ピクセルを描画
        - COLOR_BLACKを透過色として使用
        """
        pyxel.blt(
            self.x, self.y,      # 描画先座標
            0,                   # イメージバンク0
            0, 16,               # ソース画像の左上(0,16)
            24, 24,              # 幅24, 高さ24ピクセル
            COLOR_BLACK          # この色を透過色に
        )
