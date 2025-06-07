"""
ローディング画面モジュール

LoadingScene クラスは、ステージ開始前のローディング画面を制御し、
ユーザーの ENTER キー入力をトリガーにフェードアウト演出を行い、
次のステージへシーン遷移を行います。
"""

import pygame  # サウンド(BGM)管理用
import pyxel   # レトロゲームエンジン（Pyxel）を利用

# 定数や画像・シーン名のインポート
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
        loading_image (pyxel.Image): ローディング画面表示用のイメージオブジェクト
    """

    def __init__(self, game):
        """
        LoadingScene インスタンスを初期化する

        Args:
            game: ゲーム全体の管理オブジェクト
        """
        self.game = game  # ゲーム状態管理オブジェクトを保持
        # オフスクリーン描画用のイメージバンクを生成
        # (画面サイズと同じ幅・高さでPyxel Imageを作成)
        self.loading_image = pyxel.Image(SCREEN_WIDTH, SCREEN_WIDTH)

    def start(self):
        """
        ローディング画面表示開始時の処理を行う

        - BGM を停止
        - プレイヤー種別に応じたローディング画像を読み込む
        """
        # BGM（音楽）を停止する（pygame経由）
        pygame.mixer.music.stop()

        # プレイヤーの選択パイロット種別を取得
        pilot_kind = self.game.player_state.pilot_kind

        # パイロット種別に応じて、表示する画像ファイル名を選択
        if pilot_kind == PILOT_CLARICE:
            filename = IMAGE_LOADING_PILOT1  # クラリス用
        elif pilot_kind == PILOT_ROCKY:
            filename = IMAGE_LOADING_PILOT2  # ロッキー用
        elif pilot_kind == PILOT_GENZOU:
            filename = IMAGE_LOADING_PILOT3  # ゲンゾウ用
        else:
            filename = None  # 万が一一致しない場合はNone

        # 選択された画像ファイルがあれば、それをイメージバンクに読み込む
        if filename:
            # loading_imageの(0,0)から画像を読み込む
            pyxel.Image.load(self.loading_image, x=0, y=0, filename=filename)

    def update(self):
        """
        毎フレーム呼び出される更新処理

        1. ENTER キー押下で次ステージに移行
        """
        # ENTERキー（Return）が押されたかを判定
        if pyxel.btnp(pyxel.KEY_RETURN):
            # ENTERが押された場合、シーンを次のステージへ遷移
            self.game.change_scene(SCENE_PLAY_STAGE_TWO)

    def draw(self):
        """
        毎フレーム呼び出される描画処理

        - 画面を黒でクリア
        - フェードアウト効果を dither で適用
        - ローディング用イメージを描画
        """
        # 現在フェード中かを判定し、alpha値（透明度）を決定
        # フェード中ならself.game.fade_alphaを、そうでなければ完全不透明1.0
        alpha = self.game.fade_alpha if self.game.is_fading else 1.0

        # 画面全体を黒色でクリア
        pyxel.cls(COLOR_BLACK)

        # pyxel.ditherで画面にディザ（半透明）効果を適用
        pyxel.dither(alpha)

        # ローディング画像（loading_image）の左上から、画面サイズ分を描画
        pyxel.blt(
            0, 0,                      # 描画先座標（左上）
            self.loading_image,        # 描画元イメージ
            u=0, v=0,                  # 描画元イメージの左上座標
            w=SCREEN_WIDTH,            # 描画領域の幅
            h=SCREEN_HEIGHT,           # 描画領域の高さ
        )
