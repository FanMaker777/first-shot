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
    COLOR_BLACK, PLAYER_DAMAGED_COOL_TIME, PLAYER_SKILL_COOL_TIME, PILOT_ROCKY,
)
from firstshot.entities import Blast
from firstshot.entities.bullets import DogBullet, Bullet
from firstshot.entities.bullets.missile import Missile
from firstshot.entities.pilot import genzou, rocky

class Player:
    """
    プレイヤーキャラクターを表すクラス。

    - 移動、ショット、被弾、スキル、レベルアップ、描画などの全機能を管理
    - ゲーム内のプレイヤー状態に応じて各種処理を実行
    """

    def __init__(self, game, x, y):
        """
        プレイヤーを初期化しゲームに登録する。

        Args:
            game: ゲーム全体の管理インスタンス
            x (int): 初期X座標
            y (int): 初期Y座標
        """
        self.game = game  # ゲームへの参照
        self.x = x        # X座標
        self.y = y        # Y座標
        self.shot_timer = 0  # 弾発射までの残りフレーム
        # パイロットごとに当たり判定サイズを変更
        if self.game.player_state.pilot_kind == PILOT_GENZOU:
            self.hit_area = (1, 1, 3, 3)  # ゲンゾウは当たり判定が小さい
        else:
            self.hit_area = (1, 1, 6, 6)  # 通常はやや大きめ
        self.move_speed = PLAYER_MOVE_SPEED  # 移動速度
        self.shot_interval = PLAYER_SHOT_INTERVAL_DEFAULT  # 初期ショット間隔
        self.damaged_cool_time = 0  # 被弾後の無敵時間
        self.game.player_state.auto_shot_mode = False  # オートショット初期OFF

        # ゲームのプレイヤーインスタンスに自分自身を登録
        self.game.player_state.instance = self

    def add_damage(self):
        """
        プレイヤーがダメージを受けた際の処理。

        - 無敵中は何もしない
        - クールタイム開始、弾リセット、爆発エフェクト・音再生
        - ライフ減少＆ゼロなら自機削除＋ゲームオーバーに遷移
        """
        if self.damaged_cool_time > 0:
            # 無敵時間中は被弾無効
            return
        elif self.damaged_cool_time == 0:
            # クールタイムをセット（被弾後の無敵時間付与）
            self.damaged_cool_time = PLAYER_DAMAGED_COOL_TIME

        # 全ての弾をリセット
        self.game.player_state.bullets = []  # プレイヤー弾リスト初期化
        self.game.enemy_state.bullets = []   # 敵弾リスト初期化

        # 爆発エフェクト生成
        Blast(self.game, self.x + 4, self.y + 4)
        # 爆発音再生
        self.game.sound_manager.play_se_blast()

        if self.game.player_state.life > 0:
            self.game.player_state.life -= 1  # ライフを減らす

            if self.game.player_state.life == 0:
                # ライフが尽きたので自機を消去
                self.game.player_state.instance = None
                # ゲームオーバー画面へ遷移
                self.game.change_scene(SCENE_GAMEOVER)

    def update(self):
        """
        プレイヤーの状態を毎フレーム更新する。

        - レベル判定、被弾・スキルクールタイム処理
        - オートショット切替、移動、発射、スキル発動など
        """
        self.check_level()  # レベルとショット間隔の判定・更新

        # オートショットのON/OFF切り替え
        if pyxel.btnp(pyxel.KEY_SHIFT):
            self.game.player_state.auto_shot_mode = not self.game.player_state.auto_shot_mode

        # 被弾クールタイム減少（無敵時間カウント）
        if self.damaged_cool_time > 0:
            self.damaged_cool_time -= 1

        # 発射までの待機タイマー減少
        if self.shot_timer > 0:
            self.shot_timer -= 1

        # スキルクールタイム減少
        if self.game.player_state.skill_cool_time > 0:
            self.game.player_state.skill_cool_time -= 1

            # パイロットがゲンゾウならスキル自動発動（専用処理）
            if self.game.player_state.pilot_kind == PILOT_GENZOU:
                genzou.skill(self.game)

        # スキルボタンが押され条件を満たすとスキル発動
        if (pyxel.btn(pyxel.KEY_S)
            and self.game.player_state.skill_cool_time == 0
            and self.game.player_state.skill_use_time > 0):
            self.game.player_state.skill_cool_time = PLAYER_SKILL_COOL_TIME  # クールタイム付与
            self.game.player_state.skill_use_time -= 1  # 残り使用回数減
            self.game.sound_manager.play_se_use_skill()  # スキル発動音

        # プレイヤー移動処理
        self.move()
        # プレイヤーのショット
        self.shot()

    def draw(self):
        """
        プレイヤーキャラクターを画面に描画する。

        - イメージバンク0の(0,0)から8x8ピクセルをself.x,self.yに描画
        - COLOR_BLACKを透過色として利用
        """
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, COLOR_BLACK)

    def check_level(self):
        """
        プレイヤーレベルを経験値から判定し、ショット間隔・レベル値を更新する。
        """
        if self.game.player_state.exp >= 3000:
            self.game.player_state.lv = 5
            self.shot_interval = PLAYER_SHOT_INTERVAL_LV5
        elif self.game.player_state.exp >= 1000:
            self.game.player_state.lv = 4
            self.shot_interval = PLAYER_SHOT_INTERVAL_LV4
        elif self.game.player_state.exp >= 64:
            self.game.player_state.lv = 3
            self.shot_interval = PLAYER_SHOT_INTERVAL_LV3
        elif self.game.player_state.exp >= 8:
            self.game.player_state.lv = 2
            self.shot_interval = PLAYER_SHOT_INTERVAL_LV2

    def move(self):
        """
        キー入力に従って自機を移動させ、画面外に出ないよう制限する。
        """
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.move_speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.move_speed
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.move_speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.move_speed

        # 画面外に出ないよう、座標に下限・上限を設定
        self.x = max(self.x, 0)
        self.x = min(self.x, PLAYER_BOUNDARY_X_MAX)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - 8)

    def shot(self):
        """
            プレイヤーのショットを発生させる
        """
        # ショット発射判定（オートまたはスペース押し・タイマー0）
        if (self.game.player_state.auto_shot_mode or pyxel.btn(pyxel.KEY_SPACE)) and self.shot_timer == 0:

            # レベルで発射数を増やす
            if self.game.player_state.lv >= 5:
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x, self.y - 3, PLAYER_BULLET_ANGLE_UP, PLAYER_BULLET_SPEED)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x - 10, self.y - 3, PLAYER_BULLET_ANGLE_UP,
                       PLAYER_BULLET_SPEED)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x + 10, self.y - 3, PLAYER_BULLET_ANGLE_UP,
                       PLAYER_BULLET_SPEED)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x + 15, self.y - 3, PLAYER_BULLET_ANGLE_LEFT,
                       PLAYER_BULLET_SPEED)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x - 15, self.y - 3, PLAYER_BULLET_ANGLE_RIGHT,
                       PLAYER_BULLET_SPEED)
            elif self.game.player_state.lv >= 3:
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x, self.y - 3, PLAYER_BULLET_ANGLE_UP, PLAYER_BULLET_SPEED)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x - 10, self.y - 3, PLAYER_BULLET_ANGLE_UP,
                       PLAYER_BULLET_SPEED)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x + 10, self.y - 3, PLAYER_BULLET_ANGLE_UP,
                       PLAYER_BULLET_SPEED)
            elif self.game.player_state.lv >= 2:
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x - 5, self.y - 3, PLAYER_BULLET_ANGLE_UP, PLAYER_BULLET_SPEED)
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x + 5, self.y - 3, PLAYER_BULLET_ANGLE_UP,
                       PLAYER_BULLET_SPEED)
            else:
                Bullet(self.game, Bullet.SIDE_PLAYER, self.x, self.y - 3, PLAYER_BULLET_ANGLE_UP, PLAYER_BULLET_SPEED)

            # ロッキーのスキル（ショットごとに発動）
            if self.game.player_state.pilot_kind == PILOT_ROCKY:
                rocky.skill(self.game, self.x, self.y)

            # 発射音再生
            self.game.sound_manager.play_se_shot()

            # ロッキーのみ発射間隔短縮
            if self.game.player_state.pilot_kind == PILOT_ROCKY:
                self.shot_timer = self.shot_interval - 1
            else:
                self.shot_timer = self.shot_interval