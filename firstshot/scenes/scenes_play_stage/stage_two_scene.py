import pygame
import pyxel

from firstshot.entities.enemies import (
    RobotFollow,
    RobotAroundShooter,
    RobotPlayerShooter,
    StageTwoBossLeft,
    StageTwoBossRight,
)
from firstshot.scenes.scenes_play_stage import PlayScene
from firstshot.constants import (
    STAGE2_BG_PATH,
    STAGE2_ENEMY_IMAGE,
    STAGE2_BOSS_IMAGE,
    BGM_STAGE2_PATH,
    STAGE2_BGM_VOLUME,
    STAGE2_BOSS_APPEAR_TIME,
    ENEMY_SPAWN_BASE,
    ENEMY_SPAWN_MIN,
    BOSS_ALERT_DURATION,
    PLAYER_START_X,
    PLAYER_START_Y,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CLEAR_COLOR,
)


# ステージ1 画面クラス
class StageTwoScene(PlayScene):

    # 画面を開始する
    def start(self):

        # プレイ状態を初期化する
        super().start()

        # ステージ画像を切り替え
        pyxel.images[1].load(0, 0, STAGE2_BG_PATH)
        # エネミー画像を切り替え
        pyxel.images[0].load(0, 16, STAGE2_ENEMY_IMAGE)
        # ボス画像を切り替え
        self.game.boss_state.image = pyxel.Image.from_image(
            STAGE2_BOSS_IMAGE, incl_colors=False
        )

        # BGMを再生する
        pygame.mixer.music.load(BGM_STAGE2_PATH)  # 音楽ファイルを読み込む
        pygame.mixer.music.set_volume(STAGE2_BGM_VOLUME)  # 音量（0.0〜1.0）
        pygame.mixer.music.play(loops=-1)  # 無限ループ再生

    def update(self):

        # 60秒経過後にボスフラグをオンにする
        if not self.game.boss_state.active and self.game.game_data.play_time >= STAGE2_BOSS_APPEAR_TIME:
            self.game.boss_state.active = True  # ボスフラグ

        # ボスフラグがオフの時、ザコ敵を出現させる
        if not self.game.boss_state.active:
            spawn_interval = max(ENEMY_SPAWN_BASE - self.game.game_data.difficulty_level * 10, ENEMY_SPAWN_MIN)
            if self.game.game_data.play_time % spawn_interval == 0:
                kind = pyxel.rndi(0, 2)
                if kind == 0:
                    RobotFollow(self.game, self.game.game_data.difficulty_level, pyxel.rndi(16, 180), -8)
                elif kind == 1:
                    RobotAroundShooter(self.game, self.game.game_data.difficulty_level, pyxel.rndi(16, 180), -8)
                elif kind == 2:
                    RobotPlayerShooter(self.game, self.game.game_data.difficulty_level, pyxel.rndi(16, 180), -8)

        # ボスフラグがオン　AND　ボスが未出現の時
        elif self.game.boss_state.active and not any(isinstance(x, StageTwoBossLeft) for x in self.game.enemy_state.enemies.copy()):
            self.game.boss_state.alert_timer = BOSS_ALERT_DURATION  # ボスアラートの表示時間を設定
            StageTwoBossLeft(self.game, 50, 18, -64) # ボスを出現させる

        # ボスフラグがオン　AND　ボスが未出現の時
        elif self.game.boss_state.active and not any(isinstance(x, StageTwoBossRight) for x in self.game.enemy_state.enemies.copy()):
            self.game.boss_state.alert_timer = BOSS_ALERT_DURATION  # ボスアラートの表示時間を設定
            StageTwoBossRight(self.game, 50, 118, -64)  # ボスを出現させる

        # 親クラスのメソッド実行
        super().update()

    def draw(self):
        # ステージ背景を描画する
        pyxel.blt(0, 0, 1, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, CLEAR_COLOR)

        # 親クラスのメソッド実行
        super().draw()

        # 情報スペースを表示
        pyxel.rectb(200, 0, 56, SCREEN_HEIGHT, 0)
        pyxel.rect(201, 1, 54, SCREEN_HEIGHT - 2, CLEAR_COLOR)
        # 各情報を描画する
        pyxel.text(210, 32, "SCORE", 0, self.game.font)
        pyxel.text(210, 48, f"{self.game.game_data.score:05}", 0, self.game.font)
        pyxel.text(210, 112, f"EXP {self.game.player_state.exp}", 0, self.game.font)
        pyxel.text(210, 128, f"LV {self.game.player_state.lv}", 0, self.game.font)
