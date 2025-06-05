import pygame
import pyxel

from firstshot.constants import SCENE_TITLE


# ゲームオーバー画面クラス
class GameoverScene:
    # タイトル画面を初期化する
    def __init__(self, game):
        self.game = game  # ゲームクラス

    # 画面を開始する
    def start(self):

        pygame.mixer.music.stop()  # 停止
        # 画面表示時間を設定する
        self.game.display_timer = 120

        # 自機を削除する
        self.game.player = None

    def update(self):
        if self.game.display_timer > 0:  # 画面表示時間が残っている時
            self.game.display_timer -= 1
        else:  # 画面表示時間が0になった時
            self.game.change_scene(SCENE_TITLE)

    def draw(self):
        # 背景を描画する
        pyxel.blt(0, 0, 1, 0, 0, 256, 256)
        # ゲームオーバー文字を描画する
        pyxel.text(112, 128, "GAME OVER", 8, self.game.font)