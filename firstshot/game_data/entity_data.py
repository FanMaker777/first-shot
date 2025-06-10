"""
entity_data.py - ゲームエンティティの状態を管理するデータクラスを定義するモジュール
"""

from dataclasses import dataclass, field
from typing import List, Optional

import pyxel

from firstshot.constants import PLAYER_LIFE_DEFAULT, PLAYER_SKILL_USE_TIME
from firstshot.entities import Player, Blast
from firstshot.entities.bullets import Bullet
from firstshot.entities.enemies import Enemy


@dataclass
class PlayerState:
    """
    プレイヤーの状態を管理するクラス。

    Attributes:
        exp (int): プレイヤーの経験値。初期値は 0 。
        lv (int): プレイヤーのレベル。初期値は 1 。
        life (int): プレイヤーのライフ。初期値は 3 。
        skill_use_time (int): プレイヤーのスキル使用回数。
        skill_cool_time (int): プレイヤーのスキルクールタイム。
        pilot_kind (int): プレイヤーの種類を示す識別子。ゲーム内でキャラクター種別を区別するために使用。
        auto_shot_mode (bool): オートショットモード。trueの場合、モードオン。
        instance (Optional[Player]): Player クラスのインスタンスへの参照。未生成時は None。
        bullets (List[Bullet]): プレイヤーが発射した弾丸（Bullet インスタンス）の一覧。
    """
    exp: int = 0
    lv: int = 1
    life: int = PLAYER_LIFE_DEFAULT
    skill_use_time: int = PLAYER_SKILL_USE_TIME
    skill_cool_time: int = 0
    pilot_kind: int = 0
    auto_shot_mode = False  # オートショットモード
    instance: Optional[Player] = None
    bullets: List[Bullet] = field(default_factory=list)


@dataclass
class EnemyState:
    """
    敵キャラクター関連の状態を管理するクラス。

    Attributes:
        enemies (List[Enemy]): 画面上に存在する敵（Enemy インスタンス）のリスト。
        bullets (List[Bullet]): 敵が発射した弾丸（Bullet インスタンス）のリスト。
        blasts (List[Blast]): 敵の爆発エフェクト（Blast インスタンス）のリスト。
    """
    enemies: List[Enemy] = field(default_factory=list)
    bullets: List[Bullet] = field(default_factory=list)
    blasts: List[Blast] = field(default_factory=list)


@dataclass
class BossState:
    """
    ボスキャラクター関連の状態を管理するクラス。

    Attributes:
        active (bool): ボスが出現中かどうか。True の場合は画面上に表示されている。
        destroyed (bool): ボスが倒されたかどうか。True の場合は撃破済み。
        destroyed_stage2_right (bool): ボスが倒されたかどうか。True の場合は撃破済み。
        destroyed_stage2_left (bool): ボスが倒されたかどうか。True の場合は撃破済み。
        alert_timer (int): ボス出現前や特殊フェーズ時に使用する警告タイマー（フレーム単位）。
        image (Optional[pyxel.Image]): ボスの表示用画像（pyxel.Image）。読み込み前は None。
    """
    active: bool = False
    destroyed: bool = False
    destroyed_stage2_right: bool = False
    destroyed_stage2_left: bool = False
    alert_timer: int = 0
    image: Optional[pyxel.Image] = pyxel.Image(256, 256)
