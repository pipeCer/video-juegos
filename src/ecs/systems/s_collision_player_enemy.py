import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def system_collision_player_enemy(world: esper.World, player_entity: int, player_level_config):
    enemies_components = world.get_component(CEnemySpawner)
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    player_rect = player_surface.surface.get_rect(topleft=player_transform.position)

    for entity, enemies in enemies_components:
        index_to_remove = None
        enemies_components = enemies.enemies
        for index, enemy in enumerate(enemies_components):
            enemy_surface, enemy_transform, _, meta, tag = enemy
            enemy_rect = enemy_surface.surface.get_rect(topleft=enemy_transform.position)

            if enemy_rect.colliderect(player_rect):
                index_to_remove = index
                break
        if index_to_remove is not None:
            enemies.enemies.pop(index_to_remove)
            player_transform.position.x = player_level_config.position.x
            player_transform.position.y = player_level_config.position.y
