import pyxel

from firstshot.constants import (
    STAGE1_BG_PATH,
    STAGE1_ENEMY_IMAGE,
    STAGE1_BOSS_IMAGE,
    PLAYER_START_X,
    PLAYER_START_Y,
    STAGE1_BOSS_APPEAR_TIME,
    ENEMY_SPAWN_BASE,
    ENEMY_SPAWN_MIN,
    BOSS_ALERT_DURATION,
    BGM_STAGE1, BASE_SCORE_STAGE_ONE, BASE_EXP_STAGE_ONE, BASE_ARMOR_STAGE_ONE, BOSS_SCORE_STAGE_ONE,
    BOSS_EXP_STAGE_ONE, BOSS_ARMOR_STAGE_ONE, SCENE_LOADING, PLAYER_LIFE_DEFAULT, PLAYER_SKILL_USE_TIME,
)
from firstshot.entities import Player
from firstshot.entities.enemies.stage1 import Zigzag, AroundShooter, PlayerShooter, StageOneBoss
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
        self.game.player_state.life = PLAYER_LIFE_DEFAULT  # プレイヤーライフを初期値に戻す
        self.game.player_state.skill_cool_time = 0  # スキルクールタイムをリセット
        self.game.player_state.skill_use_time = PLAYER_SKILL_USE_TIME # スキル使用回数をリセット

        # ステージ画像を切り替え
        pyxel.images[1].load(0, 0, STAGE1_BG_PATH)
        # エネミー画像を切り替え
        pyxel.images[0].load(0, 16, STAGE1_ENEMY_IMAGE)
        # ボス画像を切り替え
        self.game.boss_state.image = pyxel.Image.from_image(
            STAGE1_BOSS_IMAGE, incl_colors=False
        )

        # BGMを再生する
        self.game.sound_manager.start_bgm_loop(BGM_STAGE1)

        # 自機を生成する
        Player(self.game, PLAYER_START_X, PLAYER_START_Y)

    def update(self):
        """フレームごとの更新処理。"""

        # ボス撃破フラグがTrueの場合、次のステージに移行する
        if not self.game.game_data.cleared_stage_one and self.game.boss_state.destroyed:
            # ステージクリアフラグをオンにする
            self.game.game_data.cleared_stage_one = True

        if self.game.game_data.cleared_stage_one:
            super().stagestruck(SCENE_LOADING)
            return

        # 設定時間後にボスフラグをオンにする
        if not self.game.boss_state.active and self.game.game_data.play_time >= STAGE1_BOSS_APPEAR_TIME:
            self.game.boss_state.active = True  # ボスフラグ

        # 獲得スコアを算出
        score = BASE_SCORE_STAGE_ONE * self.game.game_data.difficulty_level
        # 獲得経験値を算出
        exp = BASE_EXP_STAGE_ONE * self.game.game_data.difficulty_level
        # 装甲を算出
        armor = BASE_ARMOR_STAGE_ONE + self.game.game_data.difficulty_level

        # ボスフラグがオフの時、ザコ敵を出現させる
        if not self.game.boss_state.active:
            spawn_interval = max(ENEMY_SPAWN_BASE - self.game.game_data.difficulty_level * 10, ENEMY_SPAWN_MIN)
            if self.game.game_data.play_time % spawn_interval == 0:
                kind = pyxel.rndi(0, 2)
                if kind == 0:
                    Zigzag(self.game, score, exp, armor, pyxel.rndi(16, 180), -8, 12, 12)
                elif kind == 1:
                    AroundShooter(self.game, score, exp, armor, pyxel.rndi(16, 180), -8, 12, 12)
                elif kind == 2:
                    PlayerShooter(self.game, score, exp, armor, pyxel.rndi(16, 180), -8, 12, 12)

        # ボスフラグがオン　AND　ボスが未出現の時
        elif self.game.boss_state.active and not any(isinstance(x, StageOneBoss) for x in self.game.enemy_state.enemies.copy()):
            # ボスアラートの表示時間を設定
            self.game.boss_state.alert_timer = BOSS_ALERT_DURATION
            # ボスを出現
            StageOneBoss(
                self.game, BOSS_SCORE_STAGE_ONE, BOSS_EXP_STAGE_ONE, BOSS_ARMOR_STAGE_ONE,
                78, -64, 64, 64)

        # 親クラスのメソッド実行
        super().update()

    def draw(self):
        """描画処理。"""
        # 親クラスのメソッド実行
        super().draw()
