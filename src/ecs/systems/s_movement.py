import pygame

import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_tag_player import CTagPlayer
from src.ecs.components.c_transform import CTransform


def system_movement(world: esper.World, delta_time: float):
    components = world.get_component(CEnemySpawner)

    for entity, enemies in components:
        for enemy in enemies.enemies:
            _, transform, speed, meta, _ = enemy
            if meta.is_spawned:
                transform.position.x += speed.speed.x * delta_time
                transform.position.y += speed.speed.y * delta_time


def system_movement_player(world: esper.World, delta_time: float, screen: pygame.Surface):
    components = world.get_components(CSpeed, CTransform, CSurface, CTagPlayer)

    for entity, (player_speed, player_transform, surface, _) in components:
        player_transform.position.x += player_speed.speed.x * delta_time
        player_transform.position.y += player_speed.speed.y * delta_time
        width, height = surface.area.size
        if player_transform.position.x < 0:
            player_transform.position.x = 0
        if player_transform.position.x > screen.get_width() - width:
            player_transform.position.x = screen.get_width() - width
        if player_transform.position.y < 0:
            player_transform.position.y = 0
        if player_transform.position.y > screen.get_height() - height:
            player_transform.position.y = screen.get_height() - height


def system_movement_bullet(world: esper.World, delta_time: float, screen: pygame.Surface):
    components = world.get_components(CSpeed, CTransform, CTagBullet)

    for entity, (bullet_speed, bullet_transform, _) in components:
        bullet_transform.position.x += bullet_speed.speed.x * delta_time
        bullet_transform.position.y += bullet_speed.speed.y * delta_time

        if (
            bullet_transform.position.x < 0
            or bullet_transform.position.y < 0
            or bullet_transform.position.x > screen.get_width()
            or bullet_transform.position.y > screen.get_height()
        ):
            world.delete_entity(entity)
            break
