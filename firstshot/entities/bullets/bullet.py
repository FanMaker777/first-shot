import pyxel

from firstshot.constants import COLOR_BLACK, PILOT_CLARICE, PLAYER_BULLET_DAMAGE


# 弾クラス
class Bullet:
    """ゲーム内の弾を表すクラス。"""
    SIDE_PLAYER = 0  # 自機の弾
    SIDE_ENEMY = 1  # 敵の弾

    # 弾を初期化してゲームに登録する
    def __init__(self, game, side, x, y, angle, speed):
        """弾を初期化しゲームに登録する。"""
        self.game = game
        self.side = side
        self.x = x
        self.y = y
        self.vx = pyxel.cos(angle) * speed
        self.vy = pyxel.sin(angle) * speed
        self.damage = PLAYER_BULLET_DAMAGE

        # 弾の種類に応じた初期化とリストへの登録を行う
        if self.side == Bullet.SIDE_PLAYER:
            self.hit_area = (2, 1, 5, 6)
            game.player_state.bullets.append(self)
        else:
            self.hit_area = (2, 2, 5, 5)
            game.enemy_state.bullets.append(self)

    # 弾にダメージを与える
    def add_damage(self):
        """弾がダメージを受けた際の処理。"""
        # 弾をリストから削除する
        if self.side == Bullet.SIDE_PLAYER:
            if self in self.game.player_state.bullets:  # 自機の弾リストに登録されている時
                self.game.player_state.bullets.remove(self)
        else:
            if self in self.game.enemy_state.bullets:  # 敵の弾リストに登録されている時
                self.game.enemy_state.bullets.remove(self)

    # 弾を更新する
    def update(self):
        """弾の移動と寿命を管理する。"""
        # 弾の座標を更新する
        # PILOT_CLARICE（クラリーチェ）の場合
        if (self.game.player_state.pilot_kind == PILOT_CLARICE
             and self.game.player_state.skill_cool_time > 0 #and　スキルクールタイムが0の場合
             and self.side == Bullet.SIDE_ENEMY): #and 敵の弾の場合
            # 弾速を減少させる
            self.x += self.vx * 0.25
            self.y += self.vy * 0.25
        else:
            self.x += self.vx
            self.y += self.vy

        # 弾が画面外に出たら弾リストから登録を削除する
        if (
            self.x <= -8
            or self.x >= pyxel.width
            or self.y <= -8
            or self.y >= pyxel.height
        ):
            if self in self.game.player_state.bullets:
                if self.side == Bullet.SIDE_PLAYER:
                    self.game.player_state.bullets.remove(self)
                else:
                    self.game.enemy_state.bullets.remove(self)

    # 弾を描画する
    def draw(self):
        """弾を描画する。"""
        src_x = 0 if self.side == Bullet.SIDE_PLAYER else 8
        pyxel.blt(self.x, self.y, 0, src_x, 8, 8, 8, COLOR_BLACK)
