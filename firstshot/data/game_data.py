"""
ゲームの設定とデータを管理するモジュール

このモジュールには、ゲームの基本設定（画面サイズやタイトル、フレームレートなど）を保持する GameConfig クラスと、
ゲームプレイ中に変動する情報（スコアやシーン名、プレイ時間など）を保持する GameData クラスを定義しています。
"""

from dataclasses import dataclass

from firstshot import constants


@dataclass
class GameConfig:
    """
    ゲームの基本設定を保持するクラス

    Attributes:
        width (int): ゲーム画面の幅（ピクセル）。デフォルトは 256。
        height (int): ゲーム画面の高さ（ピクセル）。デフォルトは 256。
        title (str): ゲームウィンドウのタイトル。デフォルトは "First Shot"。
        fps (int): フレームレート（1秒あたりのフレーム数）。デフォルトは 30。
    """
    width: int = constants.SCREEN_WIDTH      # ゲームウィンドウの幅（ピクセル）
    height: int = constants.SCREEN_HEIGHT     # ゲームウィンドウの高さ（ピクセル）
    title: str = constants.SCREEN_TITLE_TEXT  # ゲームウィンドウのタイトル
    fps: int = constants.FPS         # フレームレート（FPS）

@dataclass
class GameData:
    """
    ゲームプレイ中に変動するデータを保持するクラス

    Attributes:
        score (int): プレイヤーの現在のスコア。初期値は 0。
        scene_name (str | None): 現在表示しているシーンの名前。シーン切り替え時に使用。
        play_time (float): ゲーム開始からの経過時間（秒）。更新していく。
        difficulty_level (int): 現在の難易度レベル。0 が初期値で、ゲーム進行に応じて変化する。
        is_pause_mode (bool): 一時停止フラグ
    """
    score: int = 0                   # プレイヤーのスコア
    play_time: float = 0             # プレイ経過時間（秒
    scene_name: str = None           # 現在のシーン名（例："Title", "GamePlay", "GameOver" など） ）
    difficulty_level: int = 0        # 難易度レベル（0: イージー, 1: ノーマル, 2: ハード など）
    cleared_stage_one = False        # ステージ1クリアフラグ
    cleared_stage_two = False        # ステージ2クリアフラグ
    cleared_stage_three = False      # ステージ3クリアフラグ
    stage_clear_display_time = 0     # ステージクリア表示時間
    background = None                # 背景
    is_pause_mode: bool = False       # 一時停止フラグ
