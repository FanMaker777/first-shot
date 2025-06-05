# 衝突処理モジュール

# キャラクター同士のヒットエリアが重なっているか判定する
def check_collision(entity1, entity2):
    entity1_x1 = entity1.x + entity1.hit_area[0]
    entity1_y1 = entity1.y + entity1.hit_area[1]
    entity1_x2 = entity1.x + entity1.hit_area[2]
    entity1_y2 = entity1.y + entity1.hit_area[3]

    entity2_x1 = entity2.x + entity2.hit_area[0]
    entity2_y1 = entity2.y + entity2.hit_area[1]
    entity2_x2 = entity2.x + entity2.hit_area[2]
    entity2_y2 = entity2.y + entity2.hit_area[3]

    # キャラクター1の左端がキャラクター2の右端より右にある
    if entity1_x1 > entity2_x2:
        return False

    # キャラクター1の右端がキャラクター2の左端より左にある
    if entity1_x2 < entity2_x1:
        return False

    # キャラクター1の上端がキャラクター2の下端より下にある
    if entity1_y1 > entity2_y2:
        return False

    # キャラクター1の下端がキャラクター2の上端より上にある
    if entity1_y2 < entity2_y1:
        return False

    # 上記のどれでもなければ重なっている
    return True
