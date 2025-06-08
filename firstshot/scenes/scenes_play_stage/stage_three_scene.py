import pyxel

from firstshot.constants import (
    STAGE3_BG_PATH,
    STAGE3_ENEMY_IMAGE,
    STAGE3_BOSS_IMAGE,
    BGM_STAGE3,
    STAGE3_BOSS_APPEAR_TIME,
    ENEMY_SPAWN_BASE,
    ENEMY_SPAWN_MIN,
    BOSS_ALERT_DURATION,
    BASE_SCORE_STAGE_THREE,
    BASE_EXP_STAGE_THREE,
    BASE_ARMOR_STAGE_THREE,
    BOSS_SCORE_STAGE_THREE,
    BOSS_EXP_STAGE_THREE,
    BOSS_ARMOR_STAGE_THREE,
    SCENE_GAMEOVER,
)
from firstshot.entities.enemies.stage3 import (
    WaveShooter,
    CircleShooter,
    ChargeShooter,
    StageThreeBoss,
)
from firstshot.scenes.scenes_play_stage import PlayScene


class StageThreeScene(PlayScene):
    """ステージ3を表すシーン。"""

    def start(self):
        """シーン開始時の処理。"""
        super().start()
        pyxel.images[1].load(0, 0, STAGE3_BG_PATH)
        pyxel.images[0].load(0, 16, STAGE3_ENEMY_IMAGE)
        self.game.boss_state.image = pyxel.Image.from_image(
            STAGE3_BOSS_IMAGE, incl_colors=False
        )
        self.game.sound_manager.start_bgm_loop(BGM_STAGE3)

    def update(self):
        """フレームごとの更新処理。"""
        if self.game.boss_state.destroyed:
            self.game.game_data.cleared_stage_three = True
            self.game.change_scene(SCENE_GAMEOVER)
            return

        if not self.game.boss_state.active and self.game.game_data.play_time >= STAGE3_BOSS_APPEAR_TIME:
            self.game.boss_state.active = True

        score = BASE_SCORE_STAGE_THREE * self.game.game_data.difficulty_level
        exp = BASE_EXP_STAGE_THREE * self.game.game_data.difficulty_level
        armor = BASE_ARMOR_STAGE_THREE + self.game.game_data.difficulty_level

        if not self.game.boss_state.active:
            spawn_interval = max(ENEMY_SPAWN_BASE - self.game.game_data.difficulty_level * 10, ENEMY_SPAWN_MIN)
            if self.game.game_data.play_time % spawn_interval == 0:
                kind = pyxel.rndi(0, 2)
                if kind == 0:
                    WaveShooter(self.game, score, exp, armor, pyxel.rndi(16, 180), -8, 7, 7)
                elif kind == 1:
                    CircleShooter(self.game, score, exp, armor, pyxel.rndi(16, 180), -8, 7, 7)
                else:
                    ChargeShooter(self.game, score, exp, armor, pyxel.rndi(16, 180), -8, 7, 7)
        elif self.game.boss_state.active and not any(isinstance(e, StageThreeBoss) for e in self.game.enemy_state.enemies.copy()):
            self.game.boss_state.alert_timer = BOSS_ALERT_DURATION
            StageThreeBoss(
                self.game,
                BOSS_SCORE_STAGE_THREE,
                BOSS_EXP_STAGE_THREE,
                BOSS_ARMOR_STAGE_THREE,
                78,
                -64,
                64,
                64,
            )

        super().update()

    def draw(self):
        """描画処理。"""
        super().draw()
