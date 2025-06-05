import pyxel

from firstshot.constants import SCENE_SELECT_PILOT


# タイトル画面クラス
class TitleScene:
    # タイトル画面を初期化する
    def __init__(self, game):
        self.game = game  # ゲームクラス

    # タイトル画面を開始する
    def start(self):
        # 自機を削除する
        self.game.player = None  # プレイヤーを削除

        # 全ての弾と敵を削除する
        self.game.enemies = []  # 敵のリスト
        self.game.player_bullets = []  # 自機の弾のリスト
        self.game.enemy_bullets = []  # 敵の弾のリスト
        self.game.blasts = []  # 爆発エフェクトのリスト

        # BGMを再生する
        pyxel.playm(0, loop=True)

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            # パイロット選択画面に遷移
            self.game.change_scene(SCENE_SELECT_PILOT)

    def draw(self):
        # タイトル画面を表示
        pyxel.blt(0, 0, 2, 0, 0, 256, 256, 0)