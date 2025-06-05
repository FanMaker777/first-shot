import pyxel

from firstshot.constants import SCENE_PLAY_STAGE_TWO
from firstshot.entities import Player
from firstshot.entities.enemies import Zigzag, AroundShooter, PlayerShooter
from firstshot.entities.enemies.enemy_stage1_boss import StageOneBoss
from firstshot.scenes.scenes_play_stage import PlayScene


# ステージ1 画面クラス
class StageOneScene(PlayScene):

    # 画面を開始する
    def start(self):

        # プレイ状態を初期化する
        super().start()
        self.game.score = 0  # スコアを0に戻す
        self.game.play_time = 0  # プレイ時間を0に戻す
        self.game.level = 1  # 難易度レベルを1に戻す
        self.game.player_exp = 1000  # プレイヤー経験値を0に戻す
        self.game.player_lv = 1  # プレイヤーレベルを1に戻す

        # ステージ画像を切り替え
        pyxel.images[1].load(0, 0, "assets/background/stage.png")
        # エネミー画像を切り替え
        pyxel.images[0].load(0, 16, "assets/enemy/enemy_sheet2_size64.png")
        # ボス画像を切り替え
        self.game.boss_image = pyxel.Image.from_image("assets/enemy/boss_sheet_size192.png", incl_colors=False)

        # BGMを再生する
        pyxel.playm(1, loop=True)

        # 自機を生成する
        Player(self.game, 96, 200)

    def update(self):

        # ボス撃破フラグをTrueの場合、次のステージに移行する
        if self.game.boss_destroy_flag:
            self.game.change_scene(SCENE_PLAY_STAGE_TWO)
            return

        # 60秒経過後にボスフラグをオンにする
        if not self.game.boss_emerge_flag and self.game.play_time >= 180:
            self.game.boss_emerge_flag = True  # ボスフラグ

        # ボスフラグがオフの時、ザコ敵を出現させる
        if not self.game.boss_emerge_flag:
            spawn_interval = max(90 - self.game.level * 10, 20)
            if self.game.play_time % spawn_interval == 0:
                kind = pyxel.rndi(0, 2)
                if kind == 0:
                    Zigzag(self.game, self.game.level, pyxel.rndi(16, 180), -8)
                elif kind == 1:
                    AroundShooter(self.game, self.game.level, pyxel.rndi(16, 180), -8)
                elif kind == 2:
                    PlayerShooter(self.game, self.game.level, pyxel.rndi(16, 180), -8)

        # ボスフラグがオン　AND　ボスが未出現の時
        elif self.game.boss_emerge_flag and not any(isinstance(x, StageOneBoss) for x in self.game.enemies.copy()):
            self.game.boss_alert = 180 #ボスアラートの表示時間を設定
            StageOneBoss(self.game, 50, 78, -64) # ボスを出現させる

        # 親クラスのメソッド実行
        super().update()

    def draw(self):
        # ステージ背景を描画する
        pyxel.blt(0, 0, 1, 0, 0, 256, 256)

        # 親クラスのメソッド実行
        super().draw()

        # 情報スペースを表示
        pyxel.rectb(200, 0, 56, 256, 0)
        pyxel.rect(201, 1, 54, 254, 188)
        # 各情報を描画する
        pyxel.text(210, 32, "SCORE", 0, self.game.font)
        pyxel.text(210, 48, f"{self.game.score:05}", 0, self.game.font)
        pyxel.text(210, 112, f"EXP {self.game.player_exp}", 0, self.game.font)
        pyxel.text(210, 128, f"LV {self.game.player_lv}", 0, self.game.font)
