import pyxel

from firstshot.constants import (
    SCENE_PLAY_STAGE_ONE,
    PILOT_CLARICE,
    PILOT_ROCKY,
    PILOT_GENZOU,
    IMAGE_PILOT1,
    IMAGE_PILOT2,
    IMAGE_PILOT3,
    COLOR_BLACK,
    SCREEN_WIDTH,
    PILOT_ABILITY_GENZOU,
    PILOT_SKILL_GENZOU,
    PILOT_SKILL_ROCKY,
    PILOT_ABILITY_ROCKY,
    PILOT_SKILL_CLARICE,
    PILOT_ABILITY_CLARICE,
)


# パイロット選択画面クラス
class SelectPilotScene:
    """パイロット選択画面を管理するクラス。"""
    # 画面を初期化する
    def __init__(self, game):
        """SelectPilotScene のインスタンスを初期化する。

        Args:
            game: ゲーム全体を管理する :class:`Game` オブジェクト

        このメソッドではパイロットごとの画像を読み込み、後のフレームで
        毎回読み込むことなく高速に描画できるよう辞書に保持しておく。
        """
        self.game = game  # ゲームクラス
        # パイロットの順番
        self.pilot_kind = 0
        # パイロットのアビリティ説明文
        self.pilot_ability = ""
        # パイロットのSPスキル説明文
        self.pilot_skill = ""
        # パイロット画像のイメージパンク
        self.pilot_image = pyxel.Image(SCREEN_WIDTH, SCREEN_WIDTH)
        # 各パイロットごとの画像を保持する辞書
        self.pilot_images = {
            PILOT_CLARICE: pyxel.Image.from_image(IMAGE_PILOT1, incl_colors=False),
            PILOT_ROCKY: pyxel.Image.from_image(IMAGE_PILOT2, incl_colors=False),
            PILOT_GENZOU: pyxel.Image.from_image(IMAGE_PILOT3, incl_colors=False),
        }

    # 画面を開始する
    def start(self):
        """パイロット選択画面の表示を開始する。"""
        # パイロットの順番と初期画像・説明文を設定
        self.pilot_kind = PILOT_CLARICE
        self.pilot_image = self.pilot_images[self.pilot_kind]
        self.pilot_ability = PILOT_ABILITY_CLARICE
        self.pilot_skill = PILOT_SKILL_CLARICE

    def update(self):
        """毎フレーム呼び出される更新処理を行う。"""
        prev_kind = self.pilot_kind

        if pyxel.btnp(pyxel.KEY_RIGHT):
            # パイロットの順番を次に
            self.pilot_kind = (self.pilot_kind + 1) % 3
        if pyxel.btnp(pyxel.KEY_LEFT):
            # パイロットの順番を前に
            self.pilot_kind = (self.pilot_kind - 1) % 3

        # パイロットの順番が変更されたときのみ画像と説明文を更新
        if self.pilot_kind != prev_kind:
            if self.pilot_kind == PILOT_CLARICE:
                self.pilot_image = self.pilot_images[PILOT_CLARICE]
                self.pilot_ability = PILOT_ABILITY_CLARICE
                self.pilot_skill = PILOT_SKILL_CLARICE
            elif self.pilot_kind == PILOT_ROCKY:
                self.pilot_image = self.pilot_images[PILOT_ROCKY]
                self.pilot_ability = PILOT_ABILITY_ROCKY
                self.pilot_skill = PILOT_SKILL_ROCKY
            elif self.pilot_kind == PILOT_GENZOU:
                self.pilot_image = self.pilot_images[PILOT_GENZOU]
                self.pilot_ability = PILOT_ABILITY_GENZOU
                self.pilot_skill = PILOT_SKILL_GENZOU

        if pyxel.btnp(pyxel.KEY_RETURN):
            # パイロットの種類をgameに登録
            self.game.player_state.pilot_kind = self.pilot_kind

            # プレイ画面に遷移
            self.game.change_scene(SCENE_PLAY_STAGE_ONE)

    def draw(self):
        """選択中のパイロット画像と説明を描画する。"""
        # フェードアウト用の dither を設定し画面をクリア
        alpha = self.game.fade_alpha if self.game.is_fading else 1.0
        pyxel.cls(COLOR_BLACK)
        pyxel.dither(alpha)
        # パイロットの表示
        pyxel.blt(0, 0, self.pilot_image, 0, 0, SCREEN_WIDTH, 200)
        # メッセージの表示
        pyxel.text(5, 203, "パイロット選択(ENTERボタン)", 0,self.game.font)
        pyxel.text(5, 216, "パイロット切り替え(RIGHT・LEFTボタン)", 0,self.game.font)

        # パイロットの説明を表示
        pyxel.text(5, 229, self.pilot_ability, 0, self.game.font)
        pyxel.text(5, 242, self.pilot_skill, 0, self.game.font)

