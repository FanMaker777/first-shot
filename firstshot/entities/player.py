import pyxel

from firstshot.constants import (
    SCENE_GAMEOVER,
    PILOT_GENZOU,
    PLAYER_MOVE_SPEED,
    PLAYER_SHOT_INTERVAL_DEFAULT,
    PLAYER_SHOT_INTERVAL_LV2,
    PLAYER_SHOT_INTERVAL_LV3,
    PLAYER_SHOT_INTERVAL_LV4,
    PLAYER_SHOT_INTERVAL_LV5,
    PLAYER_BOUNDARY_X_MAX,
    PLAYER_BULLET_SPEED,
    PLAYER_BULLET_ANGLE_UP,
    PLAYER_BULLET_ANGLE_LEFT,
    PLAYER_BULLET_ANGLE_RIGHT,
    PLAYER_BULLET_ANGLE_LEFT_WIDE,
    PLAYER_BULLET_ANGLE_RIGHT_WIDE,
    COLOR_BLACK, PLAYER_DAMAGED_COOL_TIME,
)
from firstshot.entities import Blast, Bullet


# 自機クラス
class Player:
    """プレイヤーキャラクターを表すクラス。"""

    # 自機を初期化してゲームに登録する
    def __init__(self, game, x, y):
        """プレイヤーを初期化しゲームに登録する。"""
        self.game = game  # ゲームへの参照
        self.x = x  # X座標
        self.y = y  # Y座標
        self.shot_timer = 0  # 弾発射までの残り時間
        # プレイヤーのステータス
        # パイロット毎に当たり判定を変更する
        if self.game.player_state.pilot_kind == PILOT_GENZOU:
            self.hit_area = (1, 1, 3, 3)  # 当たり判定の領域 (x1,y1,x2,y2)
        else:
            self.hit_area = (1, 1, 6, 6) # 当たり判定の領域 (x1,y1,x2,y2)
        self.move_speed = PLAYER_MOVE_SPEED  # 移動速度
        self.shot_interval = PLAYER_SHOT_INTERVAL_DEFAULT  # 弾の発射間隔
        self.damaged_cool_time = 0  # 被弾時のクールタイム

        # ゲームに自機を登録する
        self.game.player_state.instance = self

    # 自機にダメージを与える
    def add_damage(self):
        """プレイヤーがダメージを受けた際の処理。"""
        # 被弾時のクールタイムが0より大きい場合
        if self.damaged_cool_time > 0:
            # 被弾処理を行わずアーリーリターン
            return

        # 被弾時のクールタイムが0の場合
        elif self.damaged_cool_time == 0:
            # 被弾時のクールタイムを設定
            self.damaged_cool_time = PLAYER_DAMAGED_COOL_TIME

        # 全ての弾をリセット
        self.game.player_state.bullets = []  # 自機の弾のリスト
        self.game.enemy_state.bullets = []  # 敵の弾のリスト

        # 爆発エフェクトを生成する
        Blast(self.game, self.x + 4, self.y + 4)
        # 爆発音を再生する
        self.game.sound_manager.play_se_blast()

        # プレイヤーのライフが0より大きい場合
        if self.game.player_state.life > 0:
            self.game.player_state.life -= 1 # ライフをインクリメント

            # ライフが0になった場合
            if self.game.player_state.life == 0:
                # 自機を削除する
                self.game.player_state.instance = None

                # シーンをゲームオーバー画面に変更する
                self.game.change_scene(SCENE_GAMEOVER)


    # 自機を更新する
    def update(self):
        """プレイヤーの状態を更新する。"""
        # 被弾時のクールタイムが0より大きい場合
        if self.damaged_cool_time > 0:
            # クールタイムをインクリメント
            self.damaged_cool_time -= 1

        #プレイヤーレベル判定
        if self.game.player_state.exp >= 128:
            self.game.player_state.lv = 5
            self.shot_interval = PLAYER_SHOT_INTERVAL_LV5
        elif self.game.player_state.exp >= 64:
            self.game.player_state.lv = 4
            self.shot_interval = PLAYER_SHOT_INTERVAL_LV4
        elif self.game.player_state.exp >= 16:
            self.game.player_state.lv = 3
            self.shot_interval = PLAYER_SHOT_INTERVAL_LV3
        elif self.game.player_state.exp >= 8:
            self.game.player_state.lv = 2
            self.shot_interval = PLAYER_SHOT_INTERVAL_LV2

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
        self.x = min(self.x, PLAYER_BOUNDARY_X_MAX)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - 8)

        # 弾を発射する
        if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
            self.shot_timer -= 1

        if pyxel.btn(pyxel.KEY_SPACE) and self.shot_timer == 0:
            # 自機の弾を生成する
            Bullet(
                self.game,
                Bullet.SIDE_PLAYER,
                self.x,
                self.y - 3,
                PLAYER_BULLET_ANGLE_UP,
                PLAYER_BULLET_SPEED,
            )
            # レベルアップで発射弾を増やす
            if self.game.player_state.lv >= 5:
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x - 3, self.y - 3, PLAYER_BULLET_ANGLE_LEFT, PLAYER_BULLET_SPEED)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x + 3, self.y - 3, PLAYER_BULLET_ANGLE_RIGHT, PLAYER_BULLET_SPEED)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x - 6, self.y - 3, PLAYER_BULLET_ANGLE_LEFT_WIDE, PLAYER_BULLET_SPEED)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x + 6, self.y - 3, PLAYER_BULLET_ANGLE_RIGHT_WIDE, PLAYER_BULLET_SPEED)
            elif self.game.player_state.lv >= 3:
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x - 3, self.y - 3, PLAYER_BULLET_ANGLE_LEFT, PLAYER_BULLET_SPEED)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x + 3, self.y - 3, PLAYER_BULLET_ANGLE_RIGHT, PLAYER_BULLET_SPEED)

            # 弾発射音を再生する
            self.game.sound_manager.play_se_shot()

            # 次の弾発射までの残り時間を設定する
            self.shot_timer = self.shot_interval

    # 自機を描画する
    def draw(self):
        """プレイヤーを描画する。"""
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, COLOR_BLACK)
