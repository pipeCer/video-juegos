import pygame


class CEnemyHunter:
    def __init__(self, initial_position: pygame.Vector2, distance_start_chase: float, distance_start_return: float, velocity_chase: float, velocity_return: float) -> None:
        self.initial_position = initial_position
        self.distance_start_chase = distance_start_chase
        self.distance_start_return = distance_start_return
        self.velocity_chase = velocity_chase
        self.velocity_return = velocity_return
