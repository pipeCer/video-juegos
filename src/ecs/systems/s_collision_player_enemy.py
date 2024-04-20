import esper
from src.ecs.components.c_enemy_hunter import CEnemyHunter
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_enemy import CTagEnemy
from src.ecs.components.c_transform import CTransform
from src.engine.prefabs import create_explosion
from src.utils import get_relative_area


def system_collision_player_enemy(world: esper.World, player_entity: int, player_level_config, explosion):
    enemies_components = world.get_component(CEnemySpawner)
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    player_rect = get_relative_area(player_surface.area, player_transform.position)

    for entity, enemies in enemies_components:
        index_to_remove = None
        enemies_components = enemies.enemies
        for index, enemy in enumerate(enemies_components):
            enemy_surface, enemy_transform, _, meta, tag = enemy
            enemy_rect = get_relative_area(enemy_surface.area, enemy_transform.position)

            if enemy_rect.colliderect(player_rect):
                index_to_remove = index
                create_explosion(world, explosion, enemy_transform.position)
                break
        if index_to_remove is not None:
            player_transform.position.x = player_level_config.position.x
            player_transform.position.y = player_level_config.position.y
            enemies.enemies.pop(index_to_remove)


def system_collision_player_hunter(world: esper.World, player_entity: int, player_level_config, explosion):
    enemies_components = world.get_components(CTransform, CSurface, CEnemyHunter, CTagEnemy)
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    player_rect = get_relative_area(player_surface.area, player_transform.position)

    for entity, enemies in enemies_components:
        enemy_transform, enemy_surface, enemy_hunter, enemy_tag = enemies
        if enemy_tag.enemy_type == "Hunter":
            enemy_rect = get_relative_area(enemy_surface.area, enemy_transform.position)

            if enemy_rect.colliderect(player_rect):
                create_explosion(world, explosion, enemy_transform.position)
                world.delete_entity(entity)
                player_transform.position.x = player_level_config.position.x - player_surface.area.width / 2
                player_transform.position.y = player_level_config.position.y - player_surface.area.height / 2
