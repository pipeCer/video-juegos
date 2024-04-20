from enum import Enum


class CExplosionState:
    def __init__(self):
        self.state = ExplosionState.IDLE


class ExplosionState(Enum):
    IDLE = 0
    EXPLODE = 1
