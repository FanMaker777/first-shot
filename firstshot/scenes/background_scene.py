import pyxel

from firstshot import constants


# 背景クラス
class Background:

    # 背景を初期化してゲームに登録する
    def __init__(self, game):
        self.game = game  # ゲームへの参照
        self.stars = []  # 星の座標と速度のリスト

        # 星の座標と速度を初期化してリストに登録する
        for i in range(constants.NUM_STARS):
            x = pyxel.rndi(0, pyxel.width - 1)  # X座標
            y = pyxel.rndi(0, pyxel.height - 1)  # Y座標
            vy = pyxel.rndf(1, 2.5)  # Y方向の速度
            self.stars.append((x, y, vy))  # タプルとしてリストに登録

        # ゲームに背景を登録する
        self.game.background = self

    # 背景を更新する
    def update(self):
        for i, (x, y, vy) in enumerate(self.stars):
            y += vy
            if y >= pyxel.height:  # 画面下から出たか
                y -= pyxel.height  # 画面上に戻す
            self.stars[i] = (x, y, vy)

    # 背景を描画する
    def draw(self):
        # 星を描画する
        for x, y, speed in self.stars:
            color = 12 if speed > 1.8 else 5  # 速度に応じて色を変える
            pyxel.pset(x, y, color)