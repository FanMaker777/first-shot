import pygame
import pyxel

from firstshot.constants import SCENE_TITLE, SCENE_SELECT_PILOT, SCENE_PLAY_STAGE_ONE, SCENE_GAMEOVER, \
    SCENE_PLAY_STAGE_TWO
from firstshot.logic.dialog import display_exit_dialog
from firstshot.scenes import TitleScene, GameoverScene
from firstshot.scenes.scenes_play_stage import StageOneScene, StageTwoScene
from firstshot.scenes.select_pilot_scene import SelectPilotScene
from scenes import Background


# ゲームクラス(ゲーム全体を管理するクラス)
class Game:

    def __init__(self):
        # Pyxelを初期化する
        pyxel.init(256, 256, title="First Shot", fps=30)
        # pygameのミキサーを初期化
        pygame.mixer.init()
        # ビットマップフォントの読み込み
        self.font = pyxel.Font("assets/umplus_j10r.bdf")
        # 色パレットを254色に更新
        self.color_image = pyxel.Image(256, 256)
        self.color_image = pyxel.Image.from_image("assets/color254.png", incl_colors=True)
        # リソースファイル読込
        pyxel.load("assets/first_shot.pyxres")
        pyxel.images[0].load(0, 0, "assets/imagePank/pyxel-image0.png")
        pyxel.images[2].load(0, 0, "assets/background/title.png")
        self.boss_image = pyxel.Image(256, 256)

        # ゲームの状態を初期化する
        self.score = 0  # スコア
        self.scenes = {
            SCENE_TITLE: TitleScene(self),
            SCENE_SELECT_PILOT: SelectPilotScene(self),
            SCENE_PLAY_STAGE_ONE: StageOneScene(self),
            SCENE_PLAY_STAGE_TWO: StageTwoScene(self),
            SCENE_GAMEOVER: GameoverScene(self),
        }  # シーンの辞書
        self.scene_name = None  # 現在のシーン名
        self.play_time = 0  # プレイ時間
        self.level = 0  # 難易度レベル
        self.player_exp = 0  # プレイヤー経験値
        self.player_lv = 1  # プレイヤーレベル
        self.background = None  # 背景
        self.player = None  # 自機
        self.enemies = []  # 敵のリスト
        self.boss_flag = False  # ボスフラグ
        self.boss_destroy_flag = False  # ボス撃破フラグ
        self.boss_alert = 0  # ボスアラートの表示時間
        self.player_bullets = []  # 自機の弾のリスト
        self.enemy_bullets = []  # 敵の弾のリスト
        self.blasts = []  # 爆発エフェクトのリスト
        self.is_exit_dialog = False # Escキー押下時にダイアログを出すフラグ

        # 背景の流星を生成する
        Background(self)

        # シーンをタイトル画面に変更する
        self.change_scene(SCENE_TITLE)

        # ゲームの実行を開始する
        pyxel.run(self.update, self.draw)

    # シーンを変更する
    def change_scene(self, scene_name):
        self.scene_name = scene_name
        self.scenes[self.scene_name].start()

    # ゲーム全体を更新する
    def update(self):
        # Escキーを押されたら、終了確認ダイアログを表示
        if not self.is_exit_dialog and pyxel.btnp(pyxel.KEY_E):
            self.is_exit_dialog = True
            display_exit_dialog(self)

        # 確認ダイアログ中はゲームロジックを更新しない
        if self.is_exit_dialog:
            return

        # 現在のシーンを更新する
        self.scenes[self.scene_name].update()

        # パイロット選択画面以外は背景の流星を更新する
        if self.scene_name != SCENE_SELECT_PILOT:
            self.background.update()

    # ゲーム全体を描画する
    def draw(self):
        # 画面を黒でクリアする
        pyxel.cls(188)

        # 現在のシーンを描画する
        self.scenes[self.scene_name].draw()

        # パイロット選択画面以外は背景の流星を描画する
        if self.scene_name != SCENE_SELECT_PILOT:
            self.background.draw()

