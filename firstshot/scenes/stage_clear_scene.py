"""ステージクリア画面モジュール

各ステージクリア後に"STAGE CLEAR"を表示し、次シーンへ遷移する。"""

import pygame
import pyxel

from firstshot.constants import (
    COLOR_BLACK,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCENE_LOADING,
    SCENE_GAMEOVER,
    STAGE_CLEAR_DISPLAY_TIME,
)


class StageClearScene:
    """ステージクリアメッセージを表示するシーン。"""

    def __init__(self, game):
        """インスタンスを初期化する。"""
        self.game = game

    def start(self):
        """シーン開始時の初期化処理。"""
        pygame.mixer.music.stop()
        self.game.display_timer = STAGE_CLEAR_DISPLAY_TIME

    def update(self):
        """毎フレームの更新処理。"""
        if self.game.display_timer > 0:
            self.game.display_timer -= 1
        else:
            if self.game.game_data.cleared_stage_three:
                self.game.change_scene(SCENE_GAMEOVER)
            else:
                self.game.change_scene(SCENE_LOADING)

    def draw(self):
        """画面描画処理。"""
        alpha = self.game.fade_alpha if self.game.is_fading else 1.0
        pyxel.cls(COLOR_BLACK)
        pyxel.dither(alpha)
        text = "STAGE CLEAR"
        x = (SCREEN_WIDTH - len(text) * 4) // 2
        y = SCREEN_HEIGHT // 2
        pyxel.text(x, y, text, 8, self.game.font)
