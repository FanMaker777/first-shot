"""
敵キャラクターに関する処理を定義するモジュール

このモジュールには、敵キャラクターの基底クラス Enemy が含まれており、
敵の初期化、ダメージ処理、プレイヤー方向の角度計算、生存時間の更新、
画面外判定による削除などの機能を実装しています。
"""

import pyxel

from firstshot.constants import PILOT_CLARICE  # パイロットの種別定数
from firstshot.entities import Blast  # 爆発エフェクトを管理するクラス


class Enemy:
    """
    敵キャラクターの基底クラス

    ゲーム内に出現するすべての敵はこのクラスを継承し、基本的な挙動（ダメージ処理や削除処理など）を使用します。

    Attributes:
        game: ゲーム全体の状態や管理オブジェクトを保持するインスタンス
        score (int): この敵を倒した際にプレイヤーが獲得するスコア
        exp (int): この敵を倒した際にプレイヤーが獲得する経験値
        armor (int): 敵の装甲値。
        x (int/float): 敵の現在の X 座標（画面上の位置）
        y (int/float): 敵の現在の Y 座標（画面上の位置）
        hit_area (tuple[int, int, int, int]): 敵の当たり判定領域を表すタプル (オフセットX, オフセットY, 幅, 高さ)
        life_time (int): 敵が生成されてから経過したフレーム数
    """

    def __init__(self, game, score, exp, armor, x, y, hit_area_x, hit_area_y):
        """
        敵キャラクターを初期化してゲームに登録する

        Args:
            game: ゲーム全体の状態や管理オブジェクトを保持するインスタンス
            score (int): 倒したときに獲得できるスコア
            exp (int): 倒したときに獲得できる経験値
            armor (int): 初期装甲値
            x (int/float): 生成時の X 座標
            y (int/float): 生成時の Y 座標
            hit_area_x (int): 当たり判定領域の幅
            hit_area_y (int): 当たり判定領域の高さ
        """
        self.game = game
        self.score = score            # 倒したときに獲得するスコア
        self.exp = exp                # 倒したときに獲得する経験値
        self.armor = armor            # 現在の装甲値
        self.x = x                    # 敵の X 座標
        self.y = y                    # 敵の Y 座標
        self.hit_area = (0, 0, hit_area_x, hit_area_y)  # 当たり判定領域 (オフセットX, オフセットY, 幅, 高さ)
        self.life_time = 0            # 生成されてからの経過フレーム数

        # ゲームの敵リストにこの敵を登録する
        self.game.enemy_state.enemies.append(self)

    def add_damage(self):
        """
        敵にダメージを与えた際の処理

        装甲値が残っている場合は装甲を減少させ、それ以外では敵を破壊して爆発エフェクトを生成し、
        サウンドを再生し、スコアと経験値を加算、敵リストから削除します。
        """
        if self.armor > 0:
            # 装甲が残っている場合は装甲値を 1 減らし、すぐに戻る（敵はまだ破壊されない）
            self.armor -= 1
            return

        # 装甲が 0 の場合は敵を破壊
        # 1) 爆発エフェクトの生成（敵の中央を想定してオフセットを +4 している）
        Blast(self.game, self.x + 4, self.y + 4)

        # 2) 爆発音を再生
        self.game.sound_manager.se_blast.play()

        # 3) 敵を敵リストから削除
        if self in self.game.enemy_state.enemies:
            self.game.enemy_state.enemies.remove(self)

        # 4) プレイヤーにスコアを加算
        self.game.game_data.score += self.score

        # 5) パイロットの種別に応じて経験値を加算
        #    PILOT_CLARICE（クラリーチェ）の場合は 1.1 倍の経験値を与える
        if self.game.player_state.pilot_kind == PILOT_CLARICE:
            self.game.player_state.exp += int(self.exp * 1.1)
        else:
            self.game.player_state.exp += self.exp

    def calc_player_angle(self, x, y):
        """
        プレイヤーの方向に向かうための角度を計算して返す

        Args:
            x (int/float): 計算起点となる X 座標（通常は敵の描画座標）
            y (int/float): 計算起点となる Y 座標（通常は敵の描画座標）

        Returns:
            float: プレイヤーの方向へ向かうラジアン角度。プレイヤーが存在しない場合は 90°（π/2ラジアン）を返す。
        """
        player = self.game.player_state.instance
        if player is None:
            # プレイヤーが存在しない場合は真下（90°）を向く
            return pyxel.atan2(1, 0)  # π/2 に相当する値
        else:
            # プレイヤーの座標との差を計算して角度を取得
            return pyxel.atan2(player.y - y, player.x - x)

    def add_life_time(self):
        """
        敵の生存時間を更新する

        1フレームごとに呼び出され、life_time をインクリメントすることで
        敵がどれだけ長く生存していたかを追跡します。
        """
        self.life_time += 1

    def delete_out_enemy(self):
        """
        画面外に出た敵を削除する

        敵の Y 座標が画面の高さを超えた（画面下に出た）場合、
        敵リストからこのインスタンスを削除します。
        """
        if self.y >= pyxel.height:
            if self in self.game.enemy_state.enemies:
                self.game.enemy_state.enemies.remove(self)
