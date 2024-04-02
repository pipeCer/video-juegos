import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_movement(world: esper.World, delta_time: float):
    components = world.get_component(CEnemySpawner)

    for entity, enemies in components:
        for enemy in enemies.enemies:
            _, transform, speed, meta = enemy
            if meta.is_spawned:
                transform.position.x += speed.speed.x * delta_time
                transform.position.y += speed.speed.y * delta_time
