try:
    import pyxel
except ImportError:  # pragma: no cover - pyxel is unavailable during tests
    pyxel = None

class Laser:
    """Laser attack fired in a specific direction."""

    def __init__(self, game, x, y, angle, length, duration):
        self.game = game
        self.x = x
        self.y = y
        self.angle = angle
        self.length = length
        self.timer = duration
        self.hit_area = (0, 0, 2, length)
        game.enemy_state.bullets.append(self)

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        if self.timer <= 0 and self in self.game.enemy_state.bullets:
            self.game.enemy_state.bullets.remove(self)

    def draw(self):
        if pyxel is not None:
            end_x = self.x + pyxel.cos(self.angle) * self.length
            end_y = self.y + pyxel.sin(self.angle) * self.length
            pyxel.line(self.x, self.y, end_x, end_y, 8)
