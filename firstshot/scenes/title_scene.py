import pyxel

from firstshot.constants import SCENE_SELECT_PILOT, SCREEN_WIDTH, SCREEN_HEIGHT


# タイトル画面クラス
class TitleScene:
    # タイトル画面を初期化する
    def __init__(self, game):
        self.game = game  # ゲームクラス

    # タイトル画面を開始する
    def start(self):
        # 自機を削除する
        self.game.player_state.instance = None  # プレイヤーを削除

        # 全ての弾と敵を削除する
        self.game.enemy_state.enemies = []  # 敵のリスト
        self.game.player_state.bullets = []  # 自機の弾のリスト
        self.game.enemy_state.bullets = []  # 敵の弾のリスト
        self.game.enemy_state.blasts = []  # 爆発エフェクトのリスト

        # BGMを再生する
        pyxel.playm(0, loop=True)

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN):
            # パイロット選択画面に遷移
            self.game.change_scene(SCENE_SELECT_PILOT)

    def draw(self):
        # タイトル画面を表示
        pyxel.blt(0, 0, 2, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0)
