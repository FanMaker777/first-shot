import pyxel

from firstshot.constants import SCENE_PLAY_STAGE_ONE, PILOT_CLARICE
from firstshot.entities import Blast


# 敵クラス
class Enemy:

    # 敵を初期化してゲームに登録する
    def __init__(self, game, level, x, y):
        self.game = game
        self.level = level  # 強さ
        self.x = x
        self.y = y
        self.hit_area = (0, 0, 10, 10)
        self.armor = self.level - 1  # 装甲
        self.life_time = 0  # 生存時間

        # ゲームの敵リストに登録する
        self.game.enemy_state.enemies.append(self)

    # 敵にダメージを与える
    def add_damage(self):
        if self.armor > 0:  # 装甲が残っている時
            self.armor -= 1

            # 現在のシーンがステージ1の場合
            if self.game.game_data.scene_name == SCENE_PLAY_STAGE_ONE:
                # ダメージ音を再生する
                pyxel.play(2, 1, resume=True)  # チャンネル2で割り込み再生させる
                return
            else:
                pyxel.play(2, 1) # チャンネル2で割り込みなしで再生させる

        # 爆発エフェクトを生成する
        Blast(self.game, self.x + 4, self.y + 4)

        # 現在のシーンがステージ1の場合
        if self.game.game_data.scene_name == SCENE_PLAY_STAGE_ONE:
            # 爆発音を再生する
            pyxel.play(2, 2, resume=True)  # チャンネル2で割り込み再生させる
        else:
            pyxel.play(2, 2, )  # チャンネル2で割り込みなしで再生させる

        # 敵をリストから削除する
        if self in self.game.enemy_state.enemies:  # 敵リストに登録されている時
            self.game.enemy_state.enemies.remove(self)

        # スコアを加算する
        self.game.game_data.score += self.level * 10
        # パイロット毎に経験値を加算する
        if self.game.player_state.pilot_kind == PILOT_CLARICE:
            self.game.player_state.exp += self.level * 1.1
        else:
            self.game.player_state.exp += self.level * 1

    # 自機の方向の角度を計算する
    def calc_player_angle(self, x, y):
        player = self.game.player_state.instance
        if player is None:  # 自機が存在しない時
            return 90
        else:  # 自機が存在する時
            return pyxel.atan2(player.y - y, player.x - x)

    # 敵の生存時間を計算する
    def add_life_time(self):
        # 生存時間をカウントする
        self.life_time += 1

    # 画面外にでた敵を削除する
    def delete_out_enemy(self):
        # 敵が画面下から出たら敵リストから削除する
        if self.y >= pyxel.height:  # 画面下から出たか
            if self in self.game.enemy_state.enemies:
                self.game.enemy_state.enemies.remove(self)  # 敵リストから削除する