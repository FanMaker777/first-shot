import pyxel

from firstshot.constants import (
    SCENE_TITLE,
    SCENE_SELECT_PILOT,
    SCENE_PLAY_STAGE_ONE,
    SCENE_PLAY_STAGE_TWO,
    SCENE_PLAY_STAGE_THREE,
    SCENE_GAMEOVER,
    SCENE_GAME_CLEAR,
    FONT_PATH,
    PALETTE_IMAGE_PATH,
    RESOURCE_FILE,
    IMAGE_PANK_PATH,
    TITLE_IMAGE_PATH,
    COLOR_BLACK,
    SCREEN_WIDTH,
    SCREEN_HEIGHT, SCENE_LOADING, IMAGE_MISSILE,
)
from firstshot.game_data import PlayerState, EnemyState, BossState, GameData, GameConfig
from firstshot.logic.dialog import display_exit_dialog
from firstshot.manager import SoundManager
from firstshot.scenes import (
    TitleScene,
    GameoverScene,
    GameClearScene,
    LoadingScene,
)
from firstshot.scenes.scenes_play_stage import (
    StageOneScene,
    StageTwoScene,
    StageThreeScene,
)
from firstshot.scenes.select_pilot_scene import SelectPilotScene
from scenes import Background


# ゲームクラス(ゲーム全体を管理するクラス)
class Game:
    """ゲーム全体の管理を行うクラス。"""

    def __init__(self):
        """ゲームの初期化を行う。"""
        # ゲームの状態を初期化する
        # 各サブコンポーネントの状態だけを持つ
        self.game_config = GameConfig()
        self.game_data = GameData()
        self.player_state = PlayerState()
        self.enemy_state = EnemyState()
        self.boss_state = BossState()
        self.sound_manager = SoundManager()

        # Pyxelを初期化する
        pyxel.init(self.game_config.width, self.game_config.height, title=self.game_config.title, fps=self.game_config.fps)

        # ビットマップフォントの読み込み
        self.font = pyxel.Font(FONT_PATH)
        # 色パレットを254色に更新
        self.color_image = pyxel.Image(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.color_image = pyxel.Image.from_image(PALETTE_IMAGE_PATH, incl_colors=True)
        # リソースファイル読込
        pyxel.load(RESOURCE_FILE)
        pyxel.images[0].load(0, 0, IMAGE_PANK_PATH)
        pyxel.images[2].load(0, 0, TITLE_IMAGE_PATH)
        # 特殊弾の画像読込
        self.special_bullet_image = pyxel.Image(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.Image.load(self.special_bullet_image, 0, 0, IMAGE_MISSILE)

        self.scenes = {
            SCENE_TITLE: TitleScene(self),
            SCENE_SELECT_PILOT: SelectPilotScene(self),
            SCENE_LOADING: LoadingScene(self),
            SCENE_PLAY_STAGE_ONE: StageOneScene(self),
            SCENE_PLAY_STAGE_TWO: StageTwoScene(self),
            SCENE_PLAY_STAGE_THREE: StageThreeScene(self),
            SCENE_GAMEOVER: GameoverScene(self),
            SCENE_GAME_CLEAR: GameClearScene(self),
        }  # シーンの辞書

        # フェードアウト用のパラメータ
        self.is_fading = False         # フェードアウト中フラグ
        self.fade_alpha = 1.0          # フェードアウトの透明度
        self.next_scene_name = None    # フェードアウト後に遷移するシーン名

        # 背景の流星を生成する
        Background(self)

        # シーンをタイトル画面に変更する（起動時は即時切り替え）
        self.change_scene(SCENE_TITLE, with_fade=False)

        # ゲームの実行を開始する
        pyxel.run(self.update, self.draw)

    # シーンを変更する
    def change_scene(self, scene_name, *, with_fade=True):
        """シーンを切り替える。

        Args:
            scene_name (str): 遷移先のシーン名
            with_fade (bool): True の場合フェードアウト後に遷移する
        """
        if with_fade:
            # フェードアウト用パラメータを設定
            self.next_scene_name = scene_name
            self.fade_alpha = 1.0
            self.is_fading = True
        else:
            # 即時にシーンを切り替える
            self.game_data.scene_name = scene_name
            self.scenes[self.game_data.scene_name].start()

    # ゲーム全体を更新する
    def update(self):
        """ゲーム全体の更新処理。"""
        # Escキーを押されたら、終了確認ダイアログを表示
        if not self.game_data.is_exit_mode and pyxel.btnp(pyxel.KEY_E):
            self.game_data.is_exit_mode = True
            display_exit_dialog(self)

        # 確認ダイアログ中はゲームロジックを更新しない
        if self.game_data.is_exit_mode:
            return

        # フェードアウト処理中はシーン更新を行わない
        if self.is_fading:
            if self.fade_alpha > 0:
                self.fade_alpha -= 0.075
                if self.fade_alpha < 0:
                    self.fade_alpha = 0
            else:
                # フェードアウト完了後にシーン切り替え
                pyxel.dither(1)
                self.is_fading = False
                self.game_data.scene_name = self.next_scene_name
                self.scenes[self.game_data.scene_name].start()
            return

        # 現在のシーンを更新する
        self.scenes[self.game_data.scene_name].update()

        # パイロット選択画面以外は背景の流星を更新する
        if self.game_data.scene_name != SCENE_SELECT_PILOT:
            self.game_data.background.update()

    # ゲーム全体を描画する
    def draw(self):
        """ゲーム全体の描画処理。"""
        # 画面を黒でクリアする
        pyxel.cls(COLOR_BLACK)

        if self.is_fading:
            # フェードアウト中は現在のシーンのみ描画し、dither で暗転させる
            pyxel.dither(self.fade_alpha)
            self.scenes[self.game_data.scene_name].draw()
            if self.game_data.scene_name != SCENE_SELECT_PILOT:
                self.game_data.background.draw()
            pyxel.dither(1)
            return

        # 現在のシーンを描画する
        self.scenes[self.game_data.scene_name].draw()

        # パイロット選択画面以外は背景の流星を描画する
        if self.game_data.scene_name != SCENE_SELECT_PILOT:
            self.game_data.background.draw()

