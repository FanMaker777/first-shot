import pygame
import pyxel

from firstshot.constants import (
    SCENE_TITLE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLOR_BLACK,
    GAME_CLEAR_IMAGE_PATH, BGM_GAME_CLEAR,
)


class GameClearScene:
    """ゲームクリア画面を制御するクラス。"""

    def __init__(self, game):
        """GameClearScene のインスタンスを初期化する。"""
        self.game = game
        # ゲームクリア画面に表示するイメージを格納する Image オブジェクト
        self.clear_image = pyxel.Image(SCREEN_WIDTH, SCREEN_HEIGHT)

    def start(self):
        """ゲームクリア画面の開始処理を行う。"""
        # リソースからゲームクリア画像を読み込み表示用イメージに設定
        pyxel.Image.load(self.clear_image, 0, 0, GAME_CLEAR_IMAGE_PATH)

        pygame.mixer.music.stop()  # BGM停止
        # BGMを再生する
        self.game.sound_manager.start_bgm_loop(BGM_GAME_CLEAR)

        # プレイヤーインスタンスを削除しておく
        self.game.player_state.instance = None

    def update(self):
        """毎フレームの更新処理を実行する。"""
        # ENTER キー入力でタイトル画面へ戻る
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.game.change_scene(SCENE_TITLE)

    def draw(self):
        """ゲームクリア画面を描画する。"""
        alpha = self.game.fade_alpha if self.game.is_fading else 1.0
        pyxel.cls(COLOR_BLACK)
        pyxel.dither(alpha)
        pyxel.blt(0, 0, self.clear_image, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
