# シーン(画面)モジュール

# scenesフォルダのクラスを__init__.pyでインポートすることで
#   from scenes.play_scene import PlayScene
# のように個別にインポートする代わりに
#   from scenes import PlayScene, TitleScene, GameOverScene
# のようにまとめてインポートできるようにする

from .background_scene import Background  # 背景クラス
from .gameover_scene import GameoverScene
from .loading_scene import LoadingScene
from .stage_clear_scene import StageClearScene
from .select_pilot_scene import SelectPilotScene
from .title_scene import TitleScene
