# 定数モジュール

# 背景の星の数
NUM_STARS = 15

# シーン名
SCENE_TITLE = "title"  # タイトル画面
SCENE_SELECT_PILOT = "select_pilot"  # パイロット選択画面
SCENE_PLAY_STAGE_ONE = "play_stage_one"  # ステージ１画面
SCENE_PLAY_STAGE_TWO = "play_stage_two"  # ステージ２画面
SCENE_GAMEOVER = "gameover"  # ゲームオーバー画面

# 画面設定
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
SCREEN_TITLE_TEXT = "First Shot"
FPS = 30

# カラー
CLEAR_COLOR = 188

# ファイルパス
FONT_PATH = "assets/umplus_j10r.bdf"
PALETTE_IMAGE_PATH = "assets/color254.png"
RESOURCE_FILE = "assets/first_shot.pyxres"
IMAGE_PANK_PATH = "assets/imagePank/pyxel-image0.png"
TITLE_IMAGE_PATH = "assets/background/title.png"
STAGE1_BG_PATH = "assets/background/stage.png"
STAGE2_BG_PATH = "assets/background/stage2.png"
STAGE1_ENEMY_IMAGE = "assets/enemy/enemy_sheet2_size64.png"
STAGE1_BOSS_IMAGE = "assets/enemy/boss_sheet_size192.png"
STAGE2_ENEMY_IMAGE = "assets/enemy/enemy_stage2.png"
STAGE2_BOSS_IMAGE = "assets/enemy/boss_stage2.png"
PILOT1_IMAGE = "assets/pilot/pilot1.png"
PILOT2_IMAGE = "assets/pilot/pilot2.png"
PILOT3_IMAGE = "assets/pilot/pilot3.png"
# ファイルパス(BGM)
BGM_TITLE = "assets/bgm/title.ogg"
BGM_STAGE1 = "assets/bgm/stage1.ogg"
BGM_STAGE2 = "assets/bgm/stage2.ogg"
BGM_STAGE3 = "assets/bgm/stage3.ogg"
BGM_GAME_OVER = "assets/bgm/game_over.ogg"

# パイロット
PILOT_CLARICE = 0  # クラリーチェ
PILOT_ROCKY = 1  # ロッキー
PILOT_GENZOU = 2  # ゲンゾウ

# プレイヤー設定
PLAYER_MOVE_SPEED = 2
PLAYER_SHOT_INTERVAL_DEFAULT = 12
PLAYER_SHOT_INTERVAL_LV2 = 10
PLAYER_SHOT_INTERVAL_LV3 = 8
PLAYER_SHOT_INTERVAL_LV4 = 6
PLAYER_SHOT_INTERVAL_LV5 = 4
PLAYER_START_X = 96
PLAYER_START_Y = 200
PLAYER_BOUNDARY_X_MAX = 192
PLAYER_BULLET_SPEED = 5
PLAYER_BULLET_ANGLE_UP = -90
PLAYER_BULLET_ANGLE_LEFT = -75
PLAYER_BULLET_ANGLE_RIGHT = -105
PLAYER_BULLET_ANGLE_LEFT_WIDE = -60
PLAYER_BULLET_ANGLE_RIGHT_WIDE = -120

# 爆発
BLAST_START_RADIUS = 1
BLAST_END_RADIUS = 8

# ゲーム設定
GAMEOVER_DISPLAY_TIME = 120
STAGE1_BOSS_APPEAR_TIME = 180
STAGE2_BOSS_APPEAR_TIME = 300
ENEMY_SPAWN_BASE = 90
ENEMY_SPAWN_MIN = 20
BOSS_ALERT_DURATION = 180
STAGE2_BGM_VOLUME = 0.2

# ダイアログ
EXIT_DIALOG_TITLE = "終了確認"
EXIT_DIALOG_MESSAGE = "ゲームを終了しますか？"
