import pyxel

# ステージ3用の定数・画像パス・BGM・スコアなどをインポート
from firstshot.constants import (
    IMAGE_STAGE3_BG,
    IMAGE_STAGE3_ENEMY,
    IMAGE_STAGE3_BOSS,
    BGM_STAGE3,
    STAGE3_BOSS_APPEAR_TIME,
    ENEMY_SPAWN_BASE,
    ENEMY_SPAWN_MIN,
    BOSS_ALERT_DURATION,
    BASE_SCORE_STAGE_THREE,
    BASE_EXP_STAGE_THREE,
    BASE_ARMOR_STAGE_THREE,
    BOSS_SCORE_STAGE_THREE,
    BOSS_EXP_STAGE_THREE,
    BOSS_ARMOR_STAGE_THREE,
    SCENE_GAME_CLEAR, FPS,
)

# ステージ3のエネミークラス類をインポート
from firstshot.entities.enemies.stage3 import (
    TridentShooter,   # 波型弾エネミー
    CircleShooter, # 円形弾エネミー
    ChargeShooter, # 突進エネミー
    StageThreeBoss,# ステージ3ボス
)
# プレイシーンの親クラスをインポート
from firstshot.scenes.play_stage import PlayScene


class StageThreeScene(PlayScene):
    """
    ステージ3を表すシーン。PlaySceneを継承。

    - ステージ固有の背景、敵、ボス演出、BGM管理などを担う
    - シーン開始時や毎フレームの更新、描画処理を上書き
    """

    def __init__(self, game):
        """
        シーンのインスタンス初期化

        Args:
            game: ゲーム本体の状態管理オブジェクト
        """
        super().__init__(game)  # 親クラス(PlayScene)の初期化
        self.play_time = 0      # ステージ3固有のプレイ時間カウンタ

    def start(self):
        """
        シーン開始時の初期化処理

        - プレイ状態リセット
        - 画像やBGMなどステージ3リソース読み込み
        - プレイ時間のリセット
        """
        super().start()  # 親クラス側のstartも実行（共通初期化）
        self.play_time = 0  # ステージ3独自のプレイタイムもリセット
        self.game.player_state.skill_cool_time = 0  # スキルクールタイムをリセット

        # 背景画像をイメージバンク1へロード
        pyxel.images[1].load(0, 0, IMAGE_STAGE3_BG)
        # ザコ敵画像をイメージバンク0の一部にロード
        pyxel.images[0].load(0, 16, IMAGE_STAGE3_ENEMY)
        # ボス画像をpyxel.Imageインスタンスとしてgameオブジェクトにセット
        self.game.boss_state.image = pyxel.Image.from_image(
            IMAGE_STAGE3_BOSS, incl_colors=False
        )

        # ステージ3専用BGMをループ再生
        self.game.sound_manager.start_bgm_loop(BGM_STAGE3)

    def update(self):
        """
        毎フレームごとに呼ばれる更新処理

        - プレイ時間カウント
        - ボス出現・撃破判定
        - ザコ敵のスポーン処理
        - ボスの登場処理
        """
        # ステージ3専用のプレイ時間をインクリメント
        self.play_time += 1

        # ボスが撃破済みならステージクリアフラグを立ててゲームオーバーシーンへ遷移
        if not self.game.game_data.cleared_stage_three and self.game.boss_state.destroyed:
            self.game.game_data.cleared_stage_three = True  # ステージ3クリア記録

        if self.game.game_data.cleared_stage_three:
            super().stagestruck(SCENE_GAME_CLEAR)
            return

        # 一定時間経過後にボス出現フラグをオン
        if not self.game.boss_state.active and  self.play_time >= STAGE3_BOSS_APPEAR_TIME:
            self.game.boss_state.active = True

        # 敵の能力値を難易度に応じて算出
        score = BASE_SCORE_STAGE_THREE * self.game.game_data.difficulty_level
        exp = BASE_EXP_STAGE_THREE * self.game.game_data.difficulty_level
        armor = BASE_ARMOR_STAGE_THREE + self.game.game_data.difficulty_level

        # ボスが未出現ならザコ敵を生成する処理
        if not self.game.boss_state.active:
            # ザコ出現間隔を難易度に応じて調整（最小間隔で下限あり）
            spawn_interval = max(ENEMY_SPAWN_BASE - self.game.game_data.difficulty_level * 10, ENEMY_SPAWN_MIN)
            # play_timeのタイミングで敵出現判定
            if len(self.game.enemy_state.enemies) <= 10 and self.game.game_data.play_time % spawn_interval == 0:
                kind = pyxel.rndi(0, 2)  # 敵の種類をランダム決定
                if kind == 0:
                    # 波型弾エネミー生成
                    TridentShooter(self.game, score, exp, armor, pyxel.rndi(16, 180), -8, 24, 24)
                elif kind == 1:
                    # 円形弾エネミー生成
                    CircleShooter(self.game, score, exp, armor, pyxel.rndi(16, 180), -8, 24, 24)
                else:
                    # 突進エネミー生成
                    ChargeShooter(self.game, score, exp, armor, pyxel.rndi(16, 180), -8, 24, 24)

            # BGMのサビに合わせて固定出現
            if self.play_time == FPS * 10:
                for i in range(1, 5):
                    TridentShooter(self.game, score, exp, armor, i * 40, -8, 16, 16)

            # BGMのサビに合わせて固定出現
            if self.play_time == FPS * 35:
                for i in range(1, 5):
                    CircleShooter(self.game, score, exp, armor, i * 40, -8, 16, 16)

            # BGMのサビに合わせて固定出現
            if self.play_time == FPS * 95:
                for i in range(1, 6):
                    ChargeShooter(self.game, score, exp, armor, i * 30, -8, 16, 16)

        # ボス出現フラグが立ち、かつまだボスが生成されていなければボス出現演出
        elif self.game.boss_state.active and not any(isinstance(e, StageThreeBoss) for e in self.game.enemy_state.enemies.copy()):
            self.game.boss_state.alert_timer = BOSS_ALERT_DURATION  # ボス警告タイマーセット
            self.game.enemy_state.enemies = []  # 敵のリストをクリア
            # ボスインスタンス生成（出現位置やサイズ等は定数で指定）
            StageThreeBoss(
                self.game,
                BOSS_SCORE_STAGE_THREE,
                BOSS_EXP_STAGE_THREE,
                BOSS_ARMOR_STAGE_THREE,
                36,    # x座標
                -64,   # y座標（画面外から登場）
                128,    # 幅
                128,    # 高さ
            )

        # 親クラス側のupdateも毎回呼び出し（弾、当たり判定等の共通処理）
        super().update()

    def draw(self):
        """
        描画処理。毎フレーム呼ばれる。

        - ステージ共通の描画処理は親クラスに委譲
        """
        super().draw()
