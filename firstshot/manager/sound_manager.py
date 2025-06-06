# サウンドマネージャークラス
import pygame

from firstshot.constants import MASTER_VOLUME


class SoundManager:
    """サウンド関連処理を管理するクラス。"""
    def __init__(self):
        """インスタンスを初期化する。"""
        # pygameのミキサーを初期化
        pygame.mixer.init()
        # マスター音量を設定 (0.0 から 1.0 の範囲)
        pygame.mixer.music.set_volume(MASTER_VOLUME)

    @staticmethod
    def start_bgm_loop(file_path):
        """無限ループでBGMを再生"""
        # BGMを再生する
        pygame.mixer.music.stop()  # BGMの再生を止める
        pygame.mixer.music.load(file_path)  # 音楽ファイルを読み込む
        pygame.mixer.music.play(loops=-1)  # 無限ループ再生