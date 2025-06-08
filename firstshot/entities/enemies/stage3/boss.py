import pyxel

from firstshot.constants import COLOR_BLACK, COLOR_GREEN, COLOR_DARK_GREEN
from firstshot.entities import Bullet
from firstshot.entities.enemies import Enemy


class StageThreeBoss(Enemy):
    """ステージ3のボスキャラクター。"""

    def add_damage(self):
        """ボスがダメージを受けた際の処理。"""
        super().add_damage()
        if self not in self.game.enemy_state.enemies:
            self.game.boss_state.destroyed = True

    def update(self):
        """ボスの挙動を更新する。"""
        self.add_life_time()
        if self.y < 20:
            self.y += 1.0
        else:
            if self.life_time % 60 < 30:
                self.x += 1.0
            else:
                self.x -= 1.0
        if self.life_time % 25 == 0:
            for i in range(8):
                Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, i * 45 + 22, 4)
        if self.life_time % 70 == 0:
            angle = self.calc_player_angle(self.x + 32, self.y + 32)
            Bullet(self.game, Bullet.SIDE_ENEMY, self.x + 32, self.y + 32, angle, 5)

    def draw(self):
        """ボスを描画する。"""
        pyxel.blt(self.x, self.y, self.game.boss_state.image, 0, 0, 128, 128, COLOR_DARK_GREEN)
