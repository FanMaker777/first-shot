# エンティティ(キャラクター)モジュール

# entitiesフォルダのクラスを__init__.pyでインポートすることで
#   from entities.player import Player
# のようにクラスを個別にインポートする代わりに
#   from entities import Player, Enemy1, Enemy2, Enemy3
# のようにまとめてインポートできるようにする
from .blast import Blast
from .bullet import Bullet
from .player import Player
