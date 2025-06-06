import pyxel

from firstshot.constants import SCENE_SELECT_PILOT, SCREEN_WIDTH, SCREEN_HEIGHT, BGM_TITLE


# タイトル画面クラス
class TitleScene:
    """タイトル画面を管理するクラス。"""
    # タイトル画面を初期化する
    def __init__(self, game):
        """インスタンスを初期化する。"""
        self.game = game  # ゲームクラス

    # タイトル画面を開始する
    def start(self):
        """画面開始時の処理。"""
        # 自機を削除する
        self.game.player_state.instance = None  # プレイヤーを削除

        # 全ての弾と敵を削除する
        self.game.enemy_state.enemies = []  # 敵のリスト
        self.game.player_state.bullets = []  # 自機の弾のリスト
        self.game.enemy_state.bullets = []  # 敵の弾のリスト
        self.game.enemy_state.blasts = []  # 爆発エフェクトのリスト

        # BGMを再生する
        self.game.sound_manager.start_bgm_loop(BGM_TITLE)

    def update(self):
        """画面の更新処理。"""
        if pyxel.btnp(pyxel.KEY_RETURN):
            # パイロット選択画面に遷移
            self.game.change_scene(SCENE_SELECT_PILOT)

    def draw(self):
        """画面の描画処理。"""
        # タイトル画面を表示
        pyxel.blt(0, 0, 2, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0)
