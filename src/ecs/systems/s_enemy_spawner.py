import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.systems.s_rendering import system_rendering


def system_enemy_spawner(world: esper.World, current_time: float, screen):
    components = world.get_component(CEnemySpawner)

    for entity, enemies in components:
        for enemy in enemies.enemies:
            if current_time >= enemy[-2].spawn_time:
                system_rendering(world, screen, enemy[-2].name)
