import pygame

import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_rendering(world: esper.World, screen: pygame.Surface, identifier: str):
    components = world.get_component(CEnemySpawner)

    for entity, enemies in components:
        for enemy in enemies.enemies:
            surface, transform, _, meta = enemy
            if meta.name == identifier:
                screen.blit(surface.surface, transform.position)
                meta.is_spawned = True
