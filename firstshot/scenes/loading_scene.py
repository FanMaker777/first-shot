"""
ローディング画面モジュール

LoadingScene クラスは、ステージ開始前のローディング画面を制御し、
ユーザーの ENTER キー入力をトリガーにフェードアウト演出を行い、
次のステージへシーン遷移を行います。
"""

import pygame
import pyxel

from firstshot.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLOR_BLACK,
    IMAGE_LOADING_PILOT1,
    IMAGE_LOADING_PILOT2,
    IMAGE_LOADING_PILOT3,
    PILOT_CLARICE,
    PILOT_ROCKY,
    PILOT_GENZOU,
    SCENE_PLAY_STAGE_TWO,
)


class LoadingScene:
    """
    ゲームのローディング画面を制御するクラス

    Attributes:
        game: ゲーム全体の状態や管理を行うオブジェクト
        alpha (float): フェード効果用の透明度 (1.0: 不透明 → 0.0: 完全透明)
        is_transfer_next_stage (bool): 次のステージへの移行中フラグ
        loading_image (pyxel.Image): ローディング画面表示用のイメージオブジェクト
    """

    def __init__(self, game):
        """
        LoadingScene インスタンスを初期化する

        Args:
            game: ゲーム全体の管理オブジェクト
        """
        self.game = game
        # フェード演出開始時の透明度 (1.0: 不透明)
        self.alpha = 1.0
        # 次ステージ移行中かどうかのフラグ
        self.is_transfer_next_stage = False
        # オフスクリーン描画用のイメージバンクを生成
        self.loading_image = pyxel.Image(SCREEN_WIDTH, SCREEN_WIDTH)

    def start(self):
        """
        ローディング画面表示開始時の処理を行う

        - BGM を停止
        - フェード演出用パラメータをリセット
        - プレイヤー種別に応じたローディング画像を読み込む
        """
        # BGM を停止
        pygame.mixer.music.stop()

        # フェード演出用変数を初期化
        self.alpha = 1.0
        self.is_transfer_next_stage = False

        # プレイヤー種別に応じて画像ファイル名を選択
        pilot_kind = self.game.player_state.pilot_kind
        if pilot_kind == PILOT_CLARICE:
            filename = IMAGE_LOADING_PILOT1
        elif pilot_kind == PILOT_ROCKY:
            filename = IMAGE_LOADING_PILOT2
        elif pilot_kind == PILOT_GENZOU:
            filename = IMAGE_LOADING_PILOT3
        else:
            filename = None

        # 画像が指定されていれば読み込む
        if filename:
            pyxel.Image.load(self.loading_image, x=0, y=0, filename=filename)

    def update(self):
        """
        毎フレーム呼び出される更新処理

        1. is_transfer_next_stage=True の場合、alpha を徐々に減少させてフェードアウト。
           完全に透明になったら次シーンへ遷移。
        2. ENTER キー押下で is_transfer_next_stage=False から True に切り替え、
           フェードアウト開始をトリガーする。
        """
        # フェードアウト処理
        if self.is_transfer_next_stage:
            if self.alpha > 0:
                # 透明度を徐々に減らす
                self.alpha -= 0.1
                # alpha が負にならないようクランプ
                if self.alpha < 0:
                    self.alpha = 0
            else:
                # フェードアウト完了 → シーン遷移
                if self.game.game_data.cleared_stage_one:
                    # dither を使って画面にフェード効果を適用
                    pyxel.dither(1)
                    self.game.change_scene(SCENE_PLAY_STAGE_TWO)

        # ENTER キー押下でフェードアウト開始
        if not self.is_transfer_next_stage and pyxel.btnp(pyxel.KEY_RETURN):
            self.is_transfer_next_stage = True

    def draw(self):
        """
        毎フレーム呼び出される描画処理

        - 画面を黒でクリア
        - フェードアウト効果を dither で適用
        - ローディング用イメージを描画
        """
        # 画面を黒でクリア
        pyxel.cls(COLOR_BLACK)
        # フェード効果を適用（dither モードを alpha 値に設定）
        pyxel.dither(self.alpha)
        # ローディング画面を描画
        pyxel.blt(
            0, 0,
            self.loading_image,
            u=0, v=0,
            w=SCREEN_WIDTH, h=SCREEN_HEIGHT,
        )
