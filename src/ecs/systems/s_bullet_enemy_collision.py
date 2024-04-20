import esper
from src.ecs.components.c_enemy_hunter import CEnemyHunter
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_transform import CTransform
from src.engine.prefabs import create_explosion
from src.utils import get_relative_area


def system_collision_bullet_enemy(world: esper.World, explosion):
    enemies_components = world.get_component(CEnemySpawner)
    bullet_components = world.get_components(CSurface, CTransform, CTagBullet)

    for bullet_entity, (bullet_surface, bullet_transform, _) in bullet_components:
        bullet_rect = get_relative_area(bullet_surface.area, bullet_transform.position)

        for entity, enemies in enemies_components:
            index_to_remove = None
            for index, enemy in enumerate(enemies.enemies):
                enemy_surface, enemy_transform, _, meta, _ = enemy
                enemy_rect = get_relative_area(enemy_surface.area, enemy_transform.position)
                if enemy_rect.colliderect(bullet_rect):
                    index_to_remove = index
                    create_explosion(world, explosion, enemy_transform.position)
                    break

            if index_to_remove is not None:
                enemies.enemies.pop(index_to_remove)
                world.delete_entity(bullet_entity)
                break

        hunter_components = world.get_components(CSurface, CTransform, CEnemyHunter)

        for hunter_entity, (hunter_surface, hunter_transform, _) in hunter_components:
            hunter_rect = get_relative_area(hunter_surface.area, hunter_transform.position)
            if hunter_rect.colliderect(bullet_rect):
                world.delete_entity(bullet_entity)
                world.delete_entity(hunter_entity)
                create_explosion(world, explosion, hunter_transform.position)
                break
