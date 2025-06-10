import pyxel

from firstshot.constants import COLOR_BLACK
from firstshot.entities.enemies import Enemy


# 敵クラス
class RobotFollow(Enemy):
    """プレイヤーを追跡するロボット型の敵。"""

    # 敵を更新する
    def update(self):
        """敵の挙動を更新する。"""
        # 生存時間をカウントする
        self.add_life_time()

        # 経過時間にプレイヤーを追跡する
        if self.game.player_state.instance is not None:
            if self.life_time // 30 % 3 == 0:
                if self.game.player_state.instance.x - self.x > 0:
                    self.x += pyxel.rndi(1, 2)
                else:
                    self.x -= pyxel.rndi(1, 2)

                if self.game.player_state.instance.y - self.y > 0:
                    self.y += pyxel.rndi(1, 2)
                else:
                    self.y -= pyxel.rndi(1, 2)

        # 画面外にでた敵を削除する
        self.delete_out_enemy()

    # 敵を描画する
    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 24, 20, 20, 16, COLOR_BLACK)
