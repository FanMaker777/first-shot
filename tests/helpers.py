from firstshot.game_data import PlayerState, EnemyState, BossState, GameData

class DummyGame:
    def __init__(self):
        self.game_data = GameData()
        self.player_state = PlayerState()
        self.enemy_state = EnemyState()
        self.boss_state = BossState()
        self.display_timer = 0
        self.font = None
        self.changed_scene_to = None

    def change_scene(self, scene_name):
        self.changed_scene_to = scene_name
        self.game_data.scene_name = scene_name
