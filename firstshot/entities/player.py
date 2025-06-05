import pyxel

from firstshot.constants import SCENE_GAMEOVER
from firstshot.entities import Blast, Bullet


# 自機クラス
class Player:

    # 自機を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game  # ゲームへの参照
        self.x = x  # X座標
        self.y = y  # Y座標
        self.shot_timer = 0  # 弾発射までの残り時間
        # プレイヤーのステータス
        self.hit_area = (1, 1, 6, 6)  # 当たり判定の領域 (x1,y1,x2,y2)
        self.move_speed = 2  # 移動速度
        self.shot_interval = 12 # 弾の発射間隔

        # ゲームに自機を登録する
        self.game.player = self

    # 自機にダメージを与える
    def add_damage(self):
        # 爆発エフェクトを生成する
        Blast(self.game, self.x + 4, self.y + 4)

        # BGMを止めて爆発音を再生する
        pyxel.stop()
        pyxel.play(0, 2)

        return

        # 自機を削除する
        self.game.player = None

        # シーンをゲームオーバー画面に変更する
        self.game.change_scene(SCENE_GAMEOVER)

    # 自機を更新する
    def update(self):

        #プレイヤーレベル判定
        if self.game.player_exp >= 128:
            self.game.player_lv = 5
            self.shot_interval = 4
        elif self.game.player_exp >= 64:
            self.game.player_lv = 4
            self.shot_interval = 6
        elif self.game.player_exp >= 16:
            self.game.player_lv = 3
            self.shot_interval = 8
        elif self.game.player_exp >= 8:
            self.game.player_lv = 2
            self.shot_interval = 10

        # キー入力で自機を移動させる
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.move_speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.move_speed
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.move_speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.move_speed

        # 自機が画面外に出ないようにする
        self.x = max(self.x, 0)
        self.x = min(self.x, 192)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - 8)

        # 弾を発射する
        if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
            self.shot_timer -= 1

        if pyxel.btn(pyxel.KEY_SPACE) and self.shot_timer == 0:
            # 自機の弾を生成する
            Bullet(self.game, Bullet.SIDE_PLAYER, self.x, self.y - 3, -90, 5)
            # レベルアップで発射弾を増やす
            if self.game.player_lv >= 5:
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x - 3, self.y - 3, -75, 5)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x + 3, self.y - 3, -105, 5)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x - 6, self.y - 3, -60, 5)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x + 6, self.y - 3, -120, 5)
            elif self.game.player_lv >= 3:
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x - 3, self.y - 3, -75, 5)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x + 3, self.y - 3, -105, 5)

            # 弾発射音を再生する
            pyxel.play(3, 0)

            # 次の弾発射までの残り時間を設定する
            self.shot_timer = self.shot_interval

    # 自機を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, 188)