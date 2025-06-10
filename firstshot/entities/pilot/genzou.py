from firstshot.constants import PLAYER_BULLET_ANGLE_UP
from firstshot.entities.bullets import Missile, Bullet

# 当たり判定の領域 (x1,y1,x2,y2)
hit_area = (1, 1, 3, 3)

def skill(game):
    if game.player_state.skill_cool_time % 30 == 0: # 1秒ごとに
        # 10発のミサイルを召喚
        for i in range(8):
            Missile(game, Bullet.SIDE_PLAYER, i * 25 + 5, 230, PLAYER_BULLET_ANGLE_UP, 3)