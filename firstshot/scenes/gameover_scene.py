import pyxel

from firstshot.constants import (
    SCENE_TITLE,
    GAMEOVER_DISPLAY_TIME,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BGM_GAME_OVER,
    COLOR_BLACK,
)


# ゲームオーバー画面クラス
class GameoverScene:
    """ゲームオーバー画面を制御するクラス。"""
    # タイトル画面を初期化する
    def __init__(self, game):
        """インスタンスを初期化する。"""
        self.game = game  # ゲームクラス

    # 画面を開始する
    def start(self):
        """画面開始時の処理。"""
        # BGMを再生する
        self.game.sound_manager.start_bgm_loop(BGM_GAME_OVER)
        # 画面表示時間を設定する
        self.game.display_timer = GAMEOVER_DISPLAY_TIME

        # 自機を削除する
        self.game.player_state.instance = None

    def update(self):
        """画面の更新処理。"""
        if self.game.display_timer > 0:  # 画面表示時間が残っている時
            self.game.display_timer -= 1
        else:  # 画面表示時間が0になった時
            self.game.change_scene(SCENE_TITLE)

    def draw(self):
        """画面の描画処理。"""
        # 画面を黒でクリアしフェードアウト用の dither を設定
        alpha = self.game.fade_alpha if self.game.is_fading else 1.0
        pyxel.cls(COLOR_BLACK)
        pyxel.dither(alpha)
        # 背景を描画する
        pyxel.blt(0, 0, 1, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        # ゲームオーバー文字を描画する
        pyxel.text(100, 128, "GAME OVER", 8, self.game.font)