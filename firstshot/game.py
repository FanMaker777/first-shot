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
    IMAGE_COLOR_PALETTE,
    PYXEL_RESOURCE_FILE,
    IMAGE_DEFAULT_PANK,
    IMAGE_TITLE,
    COLOR_BLACK,
    SCREEN_WIDTH,
    SCREEN_HEIGHT, SCENE_LOADING, IMAGE_MISSILE, IMAGE_DOG_BULLET,
)
from firstshot.data import PlayerState, EnemyState, BossState, GameData, GameConfig
from firstshot.manager import SoundManager
from firstshot.scenes import (
    TitleScene,
    GameoverScene,
    GameClearScene,
    LoadingScene,
)
from firstshot.scenes.play_stage import (
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
        self.config = GameConfig()
        self.data = GameData()
        self.player_state = PlayerState()
        self.enemy_state = EnemyState()
        self.boss_state = BossState()
        self.sound_manager = SoundManager()

        # Pyxelを初期化する
        pyxel.init(self.config.width, self.config.height, title=self.config.title, fps=self.config.fps)

        # ビットマップフォントの読み込み
        self.font = pyxel.Font(FONT_PATH)
        # 色パレットを254色に更新
        self.color_image = pyxel.Image(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.color_image = pyxel.Image.from_image(IMAGE_COLOR_PALETTE, incl_colors=True)
        # リソースファイル読込
        pyxel.load(PYXEL_RESOURCE_FILE)
        pyxel.images[0].load(0, 0, IMAGE_DEFAULT_PANK)
        pyxel.images[2].load(0, 0, IMAGE_TITLE)
        # 特殊弾の画像読込
        self.special_bullet_image = pyxel.Image(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.Image.load(self.special_bullet_image, 0, 0, IMAGE_MISSILE)
        pyxel.Image.load(self.special_bullet_image, 0, 96, IMAGE_DOG_BULLET)

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
            self.data.scene_name = scene_name
            self.scenes[self.data.scene_name].start()

    # ゲーム全体を更新する
    def update(self):
        """ゲーム全体の更新処理。"""
        # Pキーを押されたら、画面を一時停止
        if pyxel.btnp(pyxel.KEY_P):
            self.data.is_pause_mode = not self.data.is_pause_mode

        # 一時停止中はゲームロジックを更新しない
        if self.data.is_pause_mode:
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
                self.data.scene_name = self.next_scene_name
                self.scenes[self.data.scene_name].start()
            return

        # 現在のシーンを更新する
        self.scenes[self.data.scene_name].update()

        # タイトル画面は背景の流星を更新する
        if self.data.scene_name == SCENE_TITLE:
            self.data.background.update()

    # ゲーム全体を描画する
    def draw(self):
        """ゲーム全体の描画処理。"""
        # 画面を黒でクリアする
        pyxel.cls(COLOR_BLACK)

        if self.is_fading:
            # フェードアウト中は現在のシーンのみ描画し、dither で暗転させる
            pyxel.dither(self.fade_alpha)
            self.scenes[self.data.scene_name].draw()
            if self.data.scene_name != SCENE_SELECT_PILOT:
                self.data.background.draw()
            pyxel.dither(1)
            return

        # 現在のシーンを描画する
        self.scenes[self.data.scene_name].draw()

        # 一時停止中を画面に表示
        if self.data.is_pause_mode:
            pyxel.text(90, 128, "PAUSE", 0, self.font)

        # タイトル画面は背景の流星を描画する
        if self.data.scene_name == SCENE_TITLE:
            self.data.background.draw()

