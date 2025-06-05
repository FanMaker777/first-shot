"""
ゲームの設定とデータを管理するモジュール

このモジュールには、ゲームの基本設定（画面サイズやタイトル、フレームレートなど）を保持する GameConfig クラスと、
ゲームプレイ中に変動する情報（スコアやシーン名、プレイ時間など）を保持する GameData クラスを定義しています。
"""

from dataclasses import dataclass

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
    width: int = 256      # ゲームウィンドウの幅（ピクセル）
    height: int = 256     # ゲームウィンドウの高さ（ピクセル）
    title: str = "First Shot"  # ゲームウィンドウのタイトル
    fps: int = 30         # フレームレート（FPS）

@dataclass
class GameData:
    """
    ゲームプレイ中に変動するデータを保持するクラス

    Attributes:
        score (int): プレイヤーの現在のスコア。初期値は 0。
        scene_name (str | None): 現在表示しているシーンの名前。シーン切り替え時に使用。
        play_time (float): ゲーム開始からの経過時間（秒）。更新していく。
        difficulty_level (int): 現在の難易度レベル。0 が初期値で、ゲーム進行に応じて変化する。
        is_exit_mode (bool): ゲーム終了処理モードに入っているかを示すフラグ。True の場合は終了処理中。
    """
    score: int = 0                   # プレイヤーのスコア
    scene_name: str = None           # 現在のシーン名（例："Title", "GamePlay", "GameOver" など）
    play_time: float = 0             # プレイ経過時間（秒）
    difficulty_level: int = 0        # 難易度レベル（0: イージー, 1: ノーマル, 2: ハード など）
    background = None  # 背景
    is_exit_mode: bool = False       # 終了処理中フラグ（True なら終了処理を行っている状態）
