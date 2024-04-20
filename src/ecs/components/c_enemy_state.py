from enum import Enum


class CEnemyState:
    def __init__(self) -> None:
        self.state = EnemyState.IDLE


class EnemyState(Enum):
    IDLE = 0
    MOVE = 1
    CHASE = 2
    RETURN = 3
