import pygame

import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_screen_bounce(world: esper.World, screen: pygame.Surface):
    components = world.get_component(CEnemySpawner)

    screen_rect = screen.get_rect()

    for entity, enemies in components:
        for enemy in enemies.enemies:
            surface, transform, speed, _, _ = enemy

            c_speed = speed
            c_transform = transform
            c_surface = surface

            surface_rect = c_surface.surface.get_rect(topleft=c_transform.position)

            if not screen_rect.contains(surface_rect):
                if surface_rect.left < 0 or surface_rect.right > screen_rect.right:
                    c_speed.speed.x *= -1
                if surface_rect.top < 0 or surface_rect.bottom > screen_rect.bottom:
                    c_speed.speed.y *= -1
                surface_rect.clamp_ip(screen_rect)
