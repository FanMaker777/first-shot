import pyxel

from firstshot.constants import CLEAR_COLOR
from firstshot.entities.enemies import Enemy


# 敵クラス
class RobotFollow(Enemy):
    """プレイヤーを追跡するロボット型の敵。"""

    # 敵を初期化してゲームに登録する
    def __init__(self, game, level, x, y):
        """敵の初期化を行う。"""
        
        super().__init__(game, level, x, y)
        self.armor += 15  # 装甲
        

    # 敵を更新する
    def update(self):
        """敵の挙動を更新する。"""
        # 生存時間をカウントする
        self.add_life_time()

        # 経過時間にプレイヤーを追跡する
        if self.life_time // 50 % 2 == 0:
            if self.game.player_state.instance.x - self.x > 0:
                self.x += 1.0
            else:
                self.x -= 1.0

            if self.game.player_state.instance.y - self.y > 0:
                self.y += 1.0
            else:
                self.y -= 1.0

        # 画面外にでた敵を削除する
        self.delete_out_enemy()

    # 敵を描画する
    def draw(self):
        """敵を描画する。"""
        pyxel.blt(self.x, self.y, 0, 24, 20, 20, 16, CLEAR_COLOR)
