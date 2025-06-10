import pyxel

from firstshot.constants import (
    IMAGE_STAGE2_BG,
    IMAGE_STAGE2_ENEMY,
    IMAGE_STAGE2_BOSS,
    BGM_STAGE2,
    STAGE2_BOSS_APPEAR_TIME,
    ENEMY_SPAWN_BASE,
    ENEMY_SPAWN_MIN,
    BOSS_ALERT_DURATION,
    BASE_SCORE_STAGE_TWO,
    BASE_EXP_STAGE_TWO,
    BASE_ARMOR_STAGE_TWO,
    BOSS_SCORE_STAGE_TWO,
    BOSS_EXP_STAGE_TWO,
    BOSS_ARMOR_STAGE_TWO,
    SCENE_LOADING, FPS,
)
from firstshot.entities.enemies.stage2 import RobotFollow, RobotAroundShooter, RobotPlayerShooter, StageTwoBossLeft, \
    StageTwoBossRight
from firstshot.scenes.scenes_play_stage import PlayScene


# ステージ1 画面クラス
class StageTwoScene(PlayScene):
    """ステージ2を表すシーン。"""

    # 画面を初期化する
    def __init__(self, game):
        """インスタンスを初期化する。"""
        super().__init__(game)
        # ステージ2固有のプレイ時間
        self.play_time = 0

    # 画面を開始する
    def start(self):
        """シーン開始時の処理。"""

        # プレイ状態を初期化する
        super().start()
        # ステージ2固有のプレイ時間をリセット
        self.play_time = 0
        self.game.player_state.skill_cool_time = 0  # スキルクールタイムをリセット
        self.game.boss_state.destroyed_stage2_left = False  # ボス撃破フラグ(左)
        self.game.boss_state.destroyed_stage2_right = False  # ボス撃破フラグ(右)

        # ステージ画像を切り替え
        pyxel.images[1].load(0, 0, IMAGE_STAGE2_BG)
        # エネミー画像を切り替え
        pyxel.images[0].load(0, 16, IMAGE_STAGE2_ENEMY)
        # ボス画像を切り替え
        self.game.boss_state.image = pyxel.Image.from_image(
            IMAGE_STAGE2_BOSS, incl_colors=False
        )

        # BGMを再生する
        self.game.sound_manager.start_bgm_loop(BGM_STAGE2)

    def update(self):
        """フレームごとの更新処理。"""
        # ステージ2固有のプレイ時間を加算
        self.play_time += 1

        # 左右のボス撃破フラグがTrueの場合
        if (not self.game.game_data.cleared_stage_two
                and self.game.boss_state.destroyed_stage2_left
                and self.game.boss_state.destroyed_stage2_right):
            # ステージクリアフラグをONに設定
            self.game.game_data.cleared_stage_two = True

        # ステージクリアフラグがONの場合
        if self.game.game_data.cleared_stage_two:
            super().stagestruck(SCENE_LOADING)
            return

        # 設定時間経過後にボスフラグをオンにする
        if not self.game.boss_state.active and self.play_time >= STAGE2_BOSS_APPEAR_TIME:
            self.game.boss_state.active = True  # ボスフラグ

        # 獲得スコアを算出
        score = BASE_SCORE_STAGE_TWO * self.game.game_data.difficulty_level
        # 獲得経験値を算出
        exp = BASE_EXP_STAGE_TWO * self.game.game_data.difficulty_level
        # 装甲を算出
        armor = BASE_ARMOR_STAGE_TWO + self.game.game_data.difficulty_level

        # ボスフラグがオフの時、ザコ敵を出現させる
        if not self.game.boss_state.active:
            spawn_interval = max(ENEMY_SPAWN_BASE - self.game.game_data.difficulty_level * 10, ENEMY_SPAWN_MIN)
            if len(self.game.enemy_state.enemies) <= 10 and self.game.game_data.play_time % spawn_interval == 0:
                kind = pyxel.rndi(0, 2)
                if kind == 0:
                    RobotFollow(self.game, score, exp, armor, pyxel.rndi(16, 180), -8, 16, 16)
                elif kind == 1:
                    RobotAroundShooter(self.game, score, exp, armor, pyxel.rndi(16, 180), -8, 16, 16)
                elif kind == 2:
                    RobotPlayerShooter(self.game, score, exp, armor, pyxel.rndi(16, 180), -8, 16, 16)

            # BGMのサビに合わせて固定出現
            if self.play_time == FPS * 5:
                for i in range(1, 6):
                    RobotPlayerShooter(self.game, score, exp, armor, i * 30, -8, 16, 16)

            # BGMのサビに合わせて固定出現
            if self.play_time == FPS * 50:
                for i in range(1, 5):
                    RobotAroundShooter(self.game, score, exp, armor, i * 40, -16, 16, 16)
                for i in range(1, 5):
                    RobotFollow(self.game, score, exp, armor, i * 40, -8, 16, 16)

            # BGMのサビに合わせて固定出現
            if self.play_time == FPS * 85:
                for i in range(1, 5):
                    RobotAroundShooter(self.game, score, exp, armor, i * 40, -8, 16, 16)
                for i in range(1, 4):
                    RobotPlayerShooter(self.game, score, exp, armor, i * 50, -8, 16, 16)

        # ボスフラグがオン　AND　ボスが2体とも未出現の時
        elif (self.game.boss_state.active and
              not any(isinstance(x, StageTwoBossLeft) for x in self.game.enemy_state.enemies.copy()) and
              not any(isinstance(x, StageTwoBossRight) for x in self.game.enemy_state.enemies.copy())):
            # ボスアラートの表示時間を設定
            self.game.boss_state.alert_timer = BOSS_ALERT_DURATION
            self.game.enemy_state.enemies = []  # 敵のリストをクリア
            # ボスを出現(左側)
            StageTwoBossLeft(
                self.game, BOSS_SCORE_STAGE_TWO, BOSS_EXP_STAGE_TWO, BOSS_ARMOR_STAGE_TWO,
                18, -64, 64, 64)
            # ボスを出現(右側)
            StageTwoBossRight(
                self.game, BOSS_SCORE_STAGE_TWO, BOSS_EXP_STAGE_TWO, BOSS_ARMOR_STAGE_TWO,
                118, -64, 64, 64)

        # 親クラスのメソッド実行
        super().update()

    def draw(self):
        """描画処理。"""
        # 親クラスのメソッド実行
        super().draw()
