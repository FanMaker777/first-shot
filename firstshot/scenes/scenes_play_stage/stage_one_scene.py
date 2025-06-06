import pygame
import pyxel

from firstshot.constants import (
    SCENE_PLAY_STAGE_TWO,
    STAGE1_BG_PATH,
    STAGE1_ENEMY_IMAGE,
    STAGE1_BOSS_IMAGE,
    PLAYER_START_X,
    PLAYER_START_Y,
    STAGE1_BOSS_APPEAR_TIME,
    ENEMY_SPAWN_BASE,
    ENEMY_SPAWN_MIN,
    BOSS_ALERT_DURATION,
    BGM_STAGE1,
)
from firstshot.entities import Player
from firstshot.entities.enemies import Zigzag, AroundShooter, PlayerShooter
from firstshot.entities.enemies.enemy_stage1_boss import StageOneBoss
from firstshot.scenes.scenes_play_stage import PlayScene


# ステージ1 画面クラス
class StageOneScene(PlayScene):
    """ステージ1を表すシーン。"""

    # 画面を開始する
    def start(self):
        """シーン開始時の処理。"""

        # プレイ状態を初期化する
        super().start()
        self.game.game_data.score = 0  # スコアを0に戻す
        self.game.game_data.play_time = 0  # プレイ時間を0に戻す
        self.game.game_data.difficulty_level = 1  # 難易度レベルを1に戻す
        self.game.player_state.exp = 0  # プレイヤー経験値を0に戻す
        self.game.player_state.lv = 1  # プレイヤーレベルを1に戻す

        # ステージ画像を切り替え
        pyxel.images[1].load(0, 0, STAGE1_BG_PATH)
        # エネミー画像を切り替え
        pyxel.images[0].load(0, 16, STAGE1_ENEMY_IMAGE)
        # ボス画像を切り替え
        self.game.boss_state.image = pyxel.Image.from_image(
            STAGE1_BOSS_IMAGE, incl_colors=False
        )

        # BGMを再生する
        pygame.mixer.music.stop()  # BGMの再生を止める
        pygame.mixer.music.load(BGM_STAGE1)  # 音楽ファイルを読み込む
        pygame.mixer.music.play(loops=-1)  # 無限ループ再生

        # 自機を生成する
        Player(self.game, PLAYER_START_X, PLAYER_START_Y)

    def update(self):
        """フレームごとの更新処理。"""

        # ボス撃破フラグをTrueの場合、次のステージに移行する
        if self.game.boss_state.destroyed:
            self.game.change_scene(SCENE_PLAY_STAGE_TWO)
            return

        # 60秒経過後にボスフラグをオンにする
        if not self.game.boss_state.active and self.game.game_data.play_time >= STAGE1_BOSS_APPEAR_TIME:
            self.game.boss_state.active = True  # ボスフラグ

        # ボスフラグがオフの時、ザコ敵を出現させる
        if not self.game.boss_state.active:
            spawn_interval = max(ENEMY_SPAWN_BASE - self.game.game_data.difficulty_level * 10, ENEMY_SPAWN_MIN)
            if self.game.game_data.play_time % spawn_interval == 0:
                kind = pyxel.rndi(0, 2)
                if kind == 0:
                    Zigzag(self.game, self.game.game_data.difficulty_level, pyxel.rndi(16, 180), -8)
                elif kind == 1:
                    AroundShooter(self.game, self.game.game_data.difficulty_level, pyxel.rndi(16, 180), -8)
                elif kind == 2:
                    PlayerShooter(self.game, self.game.game_data.difficulty_level, pyxel.rndi(16, 180), -8)

        # ボスフラグがオン　AND　ボスが未出現の時
        elif self.game.boss_state.active and not any(isinstance(x, StageOneBoss) for x in self.game.enemy_state.enemies.copy()):
            self.game.boss_state.alert_timer = BOSS_ALERT_DURATION  # ボスアラートの表示時間を設定
            StageOneBoss(self.game, 50, 78, -64) # ボスを出現させる

        # 親クラスのメソッド実行
        super().update()

    def draw(self):
        """描画処理。"""
        # 親クラスのメソッド実行
        super().draw()
