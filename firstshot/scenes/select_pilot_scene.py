import pyxel

from firstshot.constants import (
    SCENE_PLAY_STAGE_ONE,
    PILOT_CLARICE,
    PILOT_ROCKY,
    PILOT_GENZOU,
    PILOT1_IMAGE,
    PILOT2_IMAGE,
    PILOT3_IMAGE,
    COLOR_BLACK,
    SCREEN_WIDTH,
)


# パイロット選択画面クラス
class SelectPilotScene:
    """パイロット選択画面を管理するクラス。"""
    # 画面を初期化する
    def __init__(self, game):
        """インスタンスを初期化する。"""
        self.game = game  # ゲームクラス
        # パイロットの順番
        self.pilot_kind = 0
        # パイロットのアビリティ説明文
        self.pilot_ability = ""
        # パイロットのSPスキル説明文
        self.pilot_skill = ""
        # パイロット画像のイメージパンク
        self.pilot_image = pyxel.Image(SCREEN_WIDTH, SCREEN_WIDTH)

    # 画面を開始する
    def start(self):
        """画面開始時の処理。"""
        # パイロットの順番
        self.pilot_kind = 0
        # パイロット画像をイメージパンクに読み込む
        pyxel.Image.load(self.pilot_image, x=0, y=0, filename=PILOT1_IMAGE)

    def update(self):
        """画面の更新処理。"""
        if pyxel.btnp(pyxel.KEY_RIGHT):
            # パイロットの順番を次に
            self.pilot_kind = (self.pilot_kind + 1) % 3
        if pyxel.btnp(pyxel.KEY_LEFT):
            # パイロットの順番を前に
            self.pilot_kind = (self.pilot_kind - 1) % 3

        # パイロットの画像と説明文を切り替え
        if self.pilot_kind == PILOT_CLARICE:
            pyxel.Image.load(self.pilot_image, x=0, y=0, filename=PILOT1_IMAGE)
            self.pilot_ability = "アビリティ：獲得EXPが少し増える"
            self.pilot_skill = "SPスキル：一定時間、敵と敵弾の速度が遅くなる"
        elif self.pilot_kind == PILOT_ROCKY:
            pyxel.Image.load(self.pilot_image, x=0, y=0, filename=PILOT2_IMAGE)
            self.pilot_ability = "アビリティ：アイテムのドロップ率が少し増える"
            self.pilot_skill = "SPスキル：一定時間、連射速度がアップする"
        elif self.pilot_kind == PILOT_GENZOU:
            pyxel.Image.load(self.pilot_image, x=0, y=0, filename=PILOT3_IMAGE)
            self.pilot_ability = "アビリティ：自機のアタリ判定が少し小さくなる"
            self.pilot_skill = "SPスキル：一定時間、ダメージがアップする"

        if pyxel.btnp(pyxel.KEY_RETURN):
            # パイロットの種類をgameに登録
            self.game.player_state.pilot_kind = self.pilot_kind

            # プレイ画面に遷移
            self.game.change_scene(SCENE_PLAY_STAGE_ONE)

    def draw(self):
        """画面の描画処理。"""
        # 画面をクリアする
        pyxel.cls(COLOR_BLACK)
        # パイロットの表示
        pyxel.blt(0, 0, self.pilot_image, 0, 0, SCREEN_WIDTH, 200)
        # メッセージの表示
        pyxel.text(5, 203, "パイロット選択(ENTERボタン)", 0,self.game.font)
        pyxel.text(5, 216, "パイロット切り替え(RIGHT・LEFTボタン)", 0,self.game.font)

        # パイロットの説明を表示
        pyxel.text(5, 229, self.pilot_ability, 0, self.game.font)
        pyxel.text(5, 242, self.pilot_skill, 0, self.game.font)

