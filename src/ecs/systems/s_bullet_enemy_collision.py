import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_transform import CTransform


def system_collision_bullet_enemy(world: esper.World):
    enemies_components = world.get_component(CEnemySpawner)
    bullet_components = world.get_components(CSurface, CTransform, CTagBullet)

    for bullet_entity, (bullet_surface, bullet_transform, _) in bullet_components:
        bullet_rect = bullet_surface.surface.get_rect(topleft=bullet_transform.position)

        for entity, enemies in enemies_components:
            index_to_remove = None
            for index, enemy in enumerate(enemies.enemies):
                enemy_surface, enemy_transform, _, meta, _ = enemy
                enemy_rect = enemy_surface.surface.get_rect(topleft=enemy_transform.position)

                if enemy_rect.colliderect(bullet_rect):
                    index_to_remove = index
                    break

            if index_to_remove is not None:
                enemies.enemies.pop(index_to_remove)
                world.delete_entity(bullet_entity)
                break
