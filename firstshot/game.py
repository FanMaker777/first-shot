import pygame
import pyxel

from firstshot.constants import (
    SCENE_TITLE,
    SCENE_SELECT_PILOT,
    SCENE_PLAY_STAGE_ONE,
    SCENE_PLAY_STAGE_TWO,
    SCENE_GAMEOVER,
    FONT_PATH,
    PALETTE_IMAGE_PATH,
    RESOURCE_FILE,
    IMAGE_PANK_PATH,
    TITLE_IMAGE_PATH,
    CLEAR_COLOR,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from firstshot.game_data import PlayerState, EnemyState, BossState, GameData, GameConfig
from firstshot.logic.dialog import display_exit_dialog
from firstshot.scenes import TitleScene, GameoverScene
from firstshot.scenes.scenes_play_stage import StageOneScene, StageTwoScene
from firstshot.scenes.select_pilot_scene import SelectPilotScene
from scenes import Background


# ゲームクラス(ゲーム全体を管理するクラス)
class Game:

    def __init__(self):
        # ゲームの状態を初期化する
        # 各サブコンポーネントの状態だけを持つ
        self.game_config = GameConfig()
        self.game_data = GameData()
        self.player_state = PlayerState()
        self.enemy_state = EnemyState()
        self.boss_state = BossState()

        # Pyxelを初期化する
        pyxel.init(self.game_config.width, self.game_config.height, title=self.game_config.title, fps=self.game_config.fps)
        # pygameのミキサーを初期化
        pygame.mixer.init()
        # ビットマップフォントの読み込み
        self.font = pyxel.Font(FONT_PATH)
        # 色パレットを254色に更新
        self.color_image = pyxel.Image(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.color_image = pyxel.Image.from_image(PALETTE_IMAGE_PATH, incl_colors=True)
        # リソースファイル読込
        pyxel.load(RESOURCE_FILE)
        pyxel.images[0].load(0, 0, IMAGE_PANK_PATH)
        pyxel.images[2].load(0, 0, TITLE_IMAGE_PATH)

        self.scenes = {
            SCENE_TITLE: TitleScene(self),
            SCENE_SELECT_PILOT: SelectPilotScene(self),
            SCENE_PLAY_STAGE_ONE: StageOneScene(self),
            SCENE_PLAY_STAGE_TWO: StageTwoScene(self),
            SCENE_GAMEOVER: GameoverScene(self),
        }  # シーンの辞書

        # 背景の流星を生成する
        Background(self)

        # シーンをタイトル画面に変更する
        self.change_scene(SCENE_TITLE)

        # ゲームの実行を開始する
        pyxel.run(self.update, self.draw)

    # シーンを変更する
    def change_scene(self, scene_name):
        self.game_data.scene_name = scene_name
        self.scenes[self.game_data.scene_name].start()

    # ゲーム全体を更新する
    def update(self):
        # Escキーを押されたら、終了確認ダイアログを表示
        if not self.game_data.is_exit_mode and pyxel.btnp(pyxel.KEY_E):
            self.game_data.is_exit_mode = True
            display_exit_dialog(self)

        # 確認ダイアログ中はゲームロジックを更新しない
        if self.game_data.is_exit_mode:
            return

        # 現在のシーンを更新する
        self.scenes[self.game_data.scene_name].update()

        # パイロット選択画面以外は背景の流星を更新する
        if self.game_data.scene_name != SCENE_SELECT_PILOT:
            self.game_data.background.update()

    # ゲーム全体を描画する
    def draw(self):
        # 画面を黒でクリアする
        pyxel.cls(CLEAR_COLOR)

        # 現在のシーンを描画する
        self.scenes[self.game_data.scene_name].draw()

        # パイロット選択画面以外は背景の流星を描画する
        if self.game_data.scene_name != SCENE_SELECT_PILOT:
            self.game_data.background.draw()

