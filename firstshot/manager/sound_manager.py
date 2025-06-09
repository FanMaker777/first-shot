# サウンドマネージャークラス
import pygame

from firstshot.constants import BGM_VOLUME, SE_SHOT, SE_VOLUME, SE_BLAST, SE_BLAST_VOLUME, SE_STAGE_CLEAR, \
    SE_STAGE_CLEAR_VOLUME, SE_USE_SKILL


class SoundManager:
    """サウンド関連処理を管理するクラス。"""
    def __init__(self):
        """インスタンスを初期化する。"""
        # pygameのミキサーを初期化
        pygame.mixer.init(frequency=48000, size=-16, channels=2, buffer=2048)
        # BGM音量を設定 (0.0 から 1.0 の範囲)
        pygame.mixer.music.set_volume(BGM_VOLUME)
        # seを初期化
        self._init_se()

    """サウンド関連処理を管理するクラス。"""

    def _init_se(self):
        """seを初期化する。"""
        # チャンネル数を 64 に変更
        pygame.mixer.set_num_channels(64)
        pygame.mixer.set_reserved(8)  # 先頭8チャンネル（0〜7）は自動再生に使わせない

        # ショット
        self.channel_shot = pygame.mixer.Channel(0)
        self.se_shot = pygame.mixer.Sound(SE_SHOT)
        self.se_shot.set_volume(SE_VOLUME)
        # 爆発
        self.channel_blast = pygame.mixer.Channel(1)
        self.se_blast = pygame.mixer.Sound(SE_BLAST)
        self.se_blast.set_volume(SE_BLAST_VOLUME)
        # ステージクリア
        self.channel_stage_clear = pygame.mixer.Channel(2)
        self.se_stage_clear = pygame.mixer.Sound(SE_STAGE_CLEAR)
        self.se_stage_clear.set_volume(SE_STAGE_CLEAR_VOLUME)
        # スキル使用
        self.channel_use_skill = pygame.mixer.Channel(3)
        self.se_use_skill = pygame.mixer.Sound(SE_USE_SKILL)
        self.se_use_skill.set_volume(SE_STAGE_CLEAR_VOLUME)

    def play_se_shot(self):
        """弾発射音を再生する。"""
        self.channel_shot.play(self.se_shot)

    def play_se_blast(self):
        """爆発音を再生する。"""
        self.channel_blast.play(self.se_blast)

    def play_se_stage_clear(self):
        """ステージクリア音を再生する。"""
        self.channel_stage_clear.play(self.se_stage_clear)

    def play_se_use_skill(self):
        """スキル使用音を再生する。"""
        self.channel_use_skill.play(self.se_use_skill)


    @staticmethod
    def start_bgm_loop(file_path):
        """無限ループでBGMを再生"""
        # BGMを再生する
        pygame.mixer.music.stop()  # BGMの再生を止める
        pygame.mixer.music.load(file_path)  # 音楽ファイルを読み込む
        pygame.mixer.music.play(loops=-1)  # 無限ループ再生