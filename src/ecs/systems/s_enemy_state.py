import pygame

import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_hunter import CEnemyHunter
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_enemy_state import EnemyState
from src.ecs.components.c_tag_enemy import CTagEnemy
from src.ecs.components.c_transform import CTransform


def system_enemy_state(world: esper.World, player_entity: int, delta_time: float):
    components = world.get_components(CTransform, CAnimation, CEnemyHunter, CEnemyState, CTagEnemy)
    player_transform = world.component_for_entity(player_entity, CTransform)

    for _, (c_transform, c_animation, c_enemy_hunter, c_enemy_state, _) in components:
        distance_to_player = c_transform.position.distance_to(player_transform.position)
        if c_enemy_state.state == EnemyState.IDLE:
            _handle_idle_state(c_animation, c_enemy_hunter, c_enemy_state, distance_to_player)
        elif c_enemy_state.state == EnemyState.MOVE:
            _handle_move_state(c_animation, c_enemy_state)
        elif c_enemy_state.state == EnemyState.CHASE:
            _handle_chase_state(c_transform, c_enemy_hunter, c_enemy_state, player_transform, delta_time, distance_to_player)
        elif c_enemy_state.state == EnemyState.RETURN:
            _handle_return_state(c_transform, c_enemy_hunter, c_enemy_state, delta_time)


def _handle_idle_state(c_animation: CAnimation, c_enemy_hunter: CEnemyHunter, c_enemy_state: CEnemyState, distance_to_player: pygame.Vector2):
    _set_animation(c_animation, 1)
    if distance_to_player <= c_enemy_hunter.distance_start_chase:
        c_enemy_state.state = EnemyState.MOVE


def _handle_move_state(c_animation: CAnimation, c_enemy_state: CEnemyState):
    _set_animation(c_animation, 0)
    c_enemy_state.state = EnemyState.CHASE


def _handle_chase_state(
    c_transform: CTransform,
    c_enemy_hunter: CEnemyHunter,
    c_enemy_state: CEnemyState,
    player_transform: CTransform,
    delta_time: float,
    distance_to_player: pygame.Vector2,
):
    if distance_to_player > c_enemy_hunter.distance_start_return:
        c_enemy_state.state = EnemyState.RETURN
    else:
        direction = player_transform.position - c_transform.position
        _move_towards_target(c_transform, direction, c_enemy_hunter.velocity_chase, delta_time)


def _handle_return_state(c_transform: CTransform, c_enemy_hunter: CEnemyHunter, c_enemy_state: CEnemyState, delta_time: float):
    direction = c_enemy_hunter.initial_position - c_transform.position
    if direction.magnitude_squared() > 1:
        _move_towards_target(c_transform, direction, c_enemy_hunter.velocity_return, delta_time)
    else:
        c_enemy_state.state = EnemyState.IDLE


def _move_towards_target(c_transform: CTransform, direction: pygame.Vector2, velocity: float, delta_time: float):
    direction.normalize_ip()
    c_transform.position += direction * velocity * delta_time


def _set_animation(c_animation: CAnimation, num_anim: int):
    if c_animation.current_animation == num_anim:
        return
    else:
        c_animation.current_animation = num_anim
        c_animation.current_animation_time = 0
        c_animation.current_frame = c_animation.animation_list[c_animation.current_animation].start
