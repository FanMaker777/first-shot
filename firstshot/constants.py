# 定数モジュール

# 背景の星の数
NUM_STARS = 15

# シーン名
SCENE_TITLE = "title"  # タイトル画面
SCENE_SELECT_PILOT = "select_pilot"  # パイロット選択画面
SCENE_LOADING = "loading"  # ローディング画面
SCENE_PLAY_STAGE_ONE = "play_stage_one"  # ステージ１画面
SCENE_PLAY_STAGE_TWO = "play_stage_two"  # ステージ２画面
SCENE_PLAY_STAGE_THREE = "play_stage_three"  # ステージ３画面
SCENE_GAMEOVER = "gameover"  # ゲームオーバー画面
SCENE_GAME_CLEAR = "game_clear"  # ゲームクリア画面

# 画面設定
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
SCREEN_TITLE_TEXT = "First Shot"
FPS = 30

# カラー
COLOR_BLACK = 188
COLOR_GREEN = 141
COLOR_DARK_GREEN = 122


# ファイルパス
FONT_PATH = "assets/umplus_j10r.bdf"
PALETTE_IMAGE_PATH = "assets/color254.png"
RESOURCE_FILE = "assets/first_shot.pyxres"
IMAGE_PANK_PATH = "assets/imagePank/pyxel-image0.png"
TITLE_IMAGE_PATH = "assets/background/title.png"
STAGE1_BG_PATH = "assets/background/stage.png"
STAGE2_BG_PATH = "assets/background/stage2.png"
STAGE3_BG_PATH = "assets/background/stage3.png"
GAME_CLEAR_IMAGE_PATH = "assets/background/game_clear.png"
STAGE1_ENEMY_IMAGE = "assets/enemy/enemy_sheet2_size64.png"
STAGE1_BOSS_IMAGE = "assets/enemy/boss_sheet_size192.png"
STAGE2_ENEMY_IMAGE = "assets/enemy/enemy_stage2.png"
STAGE2_BOSS_IMAGE = "assets/enemy/boss_stage2.png"
STAGE3_ENEMY_IMAGE = "assets/enemy/stage3.png"
STAGE3_BOSS_IMAGE = "assets/enemy/boss_stage3.png"
PILOT1_IMAGE = "assets/pilot/pilot1.png"
PILOT2_IMAGE = "assets/pilot/pilot2.png"
PILOT3_IMAGE = "assets/pilot/pilot3.png"
IMAGE_MISSILE = "assets/special_bullet/missile.png"
IMAGE_DOG_BULLET = "assets/special_bullet/dog_bullet.png"

# ファイルパス(ローディング画面)
IMAGE_LOADING_PILOT1 = "assets/loading/loading_pilot1.png"
IMAGE_LOADING_PILOT2 = "assets/loading/loading_pilot2.png"
IMAGE_LOADING_PILOT3 = "assets/loading/loading_pilot3.png"

# ファイルパス(BGM)
BGM_TITLE = "assets/bgm/title.ogg"
BGM_STAGE1 = "assets/bgm/stage1.ogg"
BGM_STAGE2 = "assets/bgm/stage2.ogg"
BGM_STAGE3 = "assets/bgm/stage3.ogg"
BGM_GAME_OVER = "assets/bgm/game_over.ogg"
BGM_GAME_CLEAR = "assets/bgm/game_clear.ogg"

# ファイルパス(SE)
SE_SHOT = "assets/se/shot.mp3"
SE_BLAST = "assets/se/blast.ogg"
SE_GET_ITEM = "assets/se/get_item.mp3"
SE_LEVEL_UP = "assets/se/level_up.mp3"
SE_STAGE_CLEAR = "assets/se/stage_clear.mp3"
SE_USE_SKILL = "assets/se/use_skill.mp3"


# パイロット
PILOT_CLARICE = 0  # クラリーチェ
PILOT_ROCKY = 1  # ロッキー
PILOT_GENZOU = 2  # ゲンゾウ

# プレイヤー設定
PLAYER_MOVE_SPEED = 2.5
PLAYER_LIFE_DEFAULT = 5
PLAYER_DAMAGED_COOL_TIME = FPS * 3
PLAYER_SKILL_USE_TIME = 5
PLAYER_SKILL_COOL_TIME = FPS * 10
PLAYER_SHOT_INTERVAL_DEFAULT = 12
PLAYER_SHOT_INTERVAL_LV2 = 10
PLAYER_SHOT_INTERVAL_LV3 = 8
PLAYER_SHOT_INTERVAL_LV4 = 6
PLAYER_SHOT_INTERVAL_LV5 = 4
PLAYER_START_X = 96
PLAYER_START_Y = 200
PLAYER_BOUNDARY_X_MAX = 192
PLAYER_BULLET_DAMAGE = 1
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
GAMEOVER_DISPLAY_TIME = FPS * 5
STAGE1_BOSS_APPEAR_TIME = FPS * 75
STAGE2_BOSS_APPEAR_TIME = FPS * 130
STAGE3_BOSS_APPEAR_TIME = FPS * 170
ENEMY_SPAWN_BASE = FPS * 3
ENEMY_SPAWN_MIN = FPS * 1
BOSS_ALERT_DURATION = FPS * 5
STAGE_CLEAR_DISPLAY_TIME = FPS * 5
# ゲーム設定(各ステージのスコア)
BASE_SCORE_STAGE_ONE = 100
BASE_SCORE_STAGE_TWO = 200
BASE_SCORE_STAGE_THREE = 300
BOSS_SCORE_STAGE_ONE = 10000
BOSS_SCORE_STAGE_TWO = 20000
BOSS_SCORE_STAGE_THREE = 30000
# ゲーム設定(各ステージの経験値)
BASE_EXP_STAGE_ONE = 1
BASE_EXP_STAGE_TWO = 4
BASE_EXP_STAGE_THREE = 8
BOSS_EXP_STAGE_ONE = 50
BOSS_EXP_STAGE_TWO = 250
BOSS_EXP_STAGE_THREE = 1000
# ゲーム設定(各ステージの装甲値)
BASE_ARMOR_STAGE_ONE = 1
BASE_ARMOR_STAGE_TWO = 4
BASE_ARMOR_STAGE_THREE = 8
BOSS_ARMOR_STAGE_ONE = 250
BOSS_ARMOR_STAGE_TWO = 500
BOSS_ARMOR_STAGE_THREE = 1000
# ゲーム設定(音量)
BGM_VOLUME = 0.2
SE_VOLUME = 0.1
SE_BLAST_VOLUME = 0.3
SE_STAGE_CLEAR_VOLUME = 0.8

# ダイアログ
EXIT_DIALOG_TITLE = "終了確認"
EXIT_DIALOG_MESSAGE = "ゲームを終了しますか？"
