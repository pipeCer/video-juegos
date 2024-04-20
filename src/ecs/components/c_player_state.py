from enum import Enum


class PlayerState(Enum):
    IDLE = 0
    MOVE = 1


class CPlayerState:
    def __init__(self):
        self.state = PlayerState.IDLE
