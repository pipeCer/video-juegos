from pygame import Vector2, Color

from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def create_enemy(enemy_size: Vector2,
                 enemy_color: Color,
                 enemy_position: Vector2,
                 enemy_speed: Vector2,
                 enemy_identifier: str,
                 spawn_time: int
                 ):
    enemy_surface = CSurface(enemy_size, enemy_color)
    enemy_transform = CTransform(enemy_position)
    enemy_speed = CSpeed(enemy_speed)
    enemy_identifier = CMetadata(enemy_identifier, spawn_time)

    return enemy_surface, enemy_transform, enemy_speed, enemy_identifier
