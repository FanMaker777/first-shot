import pygame
import pyxel

from firstshot.logic.collision import check_collision


# プレイ画面クラス
class PlayScene:
    # 画面を初期化する
    def __init__(self, game):
        self.game = game

    # 画面を開始する
    def start(self):
        # プレイ状態を初期化する
        self.game.enemy_state.enemies = []  # 敵のリスト
        self.game.player_state.bullets = []  # 自機の弾のリスト
        self.game.enemy_bullets = []  # 敵の弾のリスト
        self.game.blasts = []  # 爆発エフェクトのリスト
        self.game.boss_emerge_flag = False  # ボスフラグ
        self.game.boss_destroy_flag = False  # ボス撃破フラグ
        self.game.boss_alert = 0 # ボスアラートの表示時間

        pyxel.stop()  # BGMの再生を止める
        pygame.mixer.music.stop()  # 停止


    def update(self):
        self.game.play_time += 1  # プレイ時間をカウントする
        # 30秒(毎秒30フレームx30)毎に難易度を1上げる
        self.game.level = self.game.play_time // 900 + 1

        # 自機を更新する
        if self.game.player_state.instance is not None:
            self.game.player_state.instance.update()

        # 敵を更新する
        # ループ中に要素の追加・削除が行われても問題ないようにコピーしたリストを使用する
        for enemy in self.game.enemy_state.enemies.copy():
            enemy.update()

            # 自機と敵の当たり判定を行う
            if self.game.player_state.instance is not None and check_collision(self.game.player_state.instance, enemy):
                self.game.player_state.instance.add_damage()  # 自機にダメージを与える

        # 自機の弾を更新する
        for bullet in self.game.player_state.bullets.copy():
            bullet.update()

            # 自機の弾と敵の当たり判定を行う
            for enemy in self.game.enemy_state.enemies.copy():
                if check_collision(enemy, bullet):
                    bullet.add_damage()  # 自機の弾にダメージを与える
                    enemy.add_damage()  # 敵にダメージを与える

                    if self.game.player_state.instance is not None:  # 自機が存在する時
                        self.game.player_state.instance.sound_timer = 5  # 弾発射音を止める時間を設定する

        # 敵の弾を更新する
        for bullet in self.game.enemy_bullets.copy():
            bullet.update()

            # プレイヤーと敵の弾の当たり判定を行う
            if self.game.player_state.instance is not None and check_collision(self.game.player_state.instance, bullet):
                bullet.add_damage()  # 敵の弾にダメージを与える
                self.game.player_state.instance.add_damage()  # 自機にダメージを与える

        # 爆発エフェクトを更新する
        for blast in self.game.blasts.copy():
            blast.update()

    def draw(self):

        # 自機を描画する
        if self.game.player_state.instance is not None:
            self.game.player_state.instance.draw()

        # 敵を描画する
        for enemy in self.game.enemy_state.enemies:
            enemy.draw()

        # 自機の弾を描画する
        for bullet in self.game.player_state.bullets:
            bullet.draw()

        # 敵の弾を描画する
        for bullet in self.game.enemy_bullets:
            bullet.draw()

        # 爆発エフェクトを描画する
        for blast in self.game.blasts:
            blast.draw()

        # ボスアラートの表示時間が0より大きい場合
        if self.game.boss_alert > 0:
            self.game.boss_alert -= 1
            pyxel.text(100, 128, "BOSS",pyxel.rndi(0, 240) , self.game.font)