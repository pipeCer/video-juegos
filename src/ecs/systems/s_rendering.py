import pygame

import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_tag_player import CTagPlayer
from src.ecs.components.c_transform import CTransform


def system_rendering(world: esper.World, screen: pygame.Surface, identifier: str):
    components = world.get_component(CEnemySpawner)

    for entity, enemies in components:
        for enemy in enemies.enemies:
            surface, transform, _, meta, _ = enemy
            if meta.name == identifier:
                screen.blit(surface.surface, transform.position)
                meta.is_spawned = True


def system_render_square(world: esper.World, screen: pygame.Surface):
    player_components = world.get_components(CSurface, CTransform, CSpeed)

    for entity, (surface, transform, speed) in player_components:
        screen.blit(surface.surface, transform.position)
