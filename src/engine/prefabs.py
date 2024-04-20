import uuid

import pygame
from pygame import Vector2

import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_hunter import CEnemyHunter
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_tag_enemy import CTagEnemy
from src.ecs.components.c_tag_explosion import CTagExplosion
from src.ecs.components.c_tag_player import CTagPlayer
from src.ecs.components.c_transform import CTransform


def create_square(world, size, position, color, speed, tag):
    entity = world.create_entity()
    world.add_component(entity, CSurface(size, color))
    world.add_component(entity, CTransform(position))
    world.add_component(entity, CSpeed(speed))
    world.add_component(entity, tag)
    return entity


def create_sprite(world, sprite, position, **kwargs):
    entity = world.create_entity()
    world.add_component(entity, CSurface.from_surface(sprite))
    world.add_component(entity, CTransform(position))
    for _, value in kwargs.items():
        world.add_component(entity, value)
    return entity


def create_bullet_square(world: esper.World, bullet, player_position, player_surface):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player_width, player_height = player_surface.area.size
    bullet_surface = pygame.image.load(bullet.image).convert_alpha()
    bullet_width, bullet_height = bullet_surface.get_rect().size
    bullet_position = pygame.Vector2(player_position.x + player_width / 2 - (bullet_width / 2), player_position.y + player_height / 2 - (bullet_height / 2))
    direction_vector = pygame.Vector2(mouse_x - player_position.x, mouse_y - player_position.y)
    direction_vector.normalize_ip()
    bullet_velocity = direction_vector * bullet.velocity
    bullet_entity = create_sprite(
        world=world,
        sprite=bullet_surface,
        position=bullet_position,
        speed=CSpeed(bullet_velocity),
        tag=CTagBullet(),
    )
    world.add_component(bullet_entity, CTagBullet())


def create_player(world, player_config, player_spawn):
    player_surface = pygame.image.load(player_config.image).convert_alpha()
    player_size = player_surface.get_rect().size
    size = (player_size[0] / player_config.animations.number_frames, player_size[1])
    player_position = Vector2(player_spawn.position.x - (size[0] / 2), player_spawn.position.y - (size[1] / 2))
    player_speed = Vector2(0, 0)
    player_animation = CAnimation(player_config.animations)
    return create_sprite(world, player_surface, player_position, speed=CSpeed(player_speed), tag=CTagPlayer(), animation=player_animation, state=CPlayerState())


def create_enemy(enemy_type, current_enemy_surface: pygame.Surface, enemy_position: Vector2, enemy_speed: Vector2, enemy_identifier: str, spawn_time: int, **kwargs):
    enemy_surface = CSurface.from_surface(current_enemy_surface)
    enemy_transform = CTransform(enemy_position)
    enemy_speed = CSpeed(enemy_speed)
    enemy_identifier = CMetadata(f"{enemy_identifier}_{uuid.uuid4()}", spawn_time)
    enemy_tag = CTagEnemy(enemy_type=enemy_type)
    if enemy_type == "Hunter":
        enemy_config = kwargs["enemy_config"]
        enemy_hunter = CEnemyHunter(
            initial_position=enemy_position.copy(),
            distance_start_chase=enemy_config.distance_start_chase,
            distance_start_return=enemy_config.distance_start_return,
            velocity_chase=enemy_config.velocity_chase,
            velocity_return=enemy_config.velocity_return,
        )
        enemy_animation = CAnimation(enemy_config.animations)
        enemy_state = CEnemyState()
        return enemy_surface, enemy_transform, enemy_speed, enemy_identifier, enemy_tag, enemy_hunter, enemy_animation, enemy_state
    return enemy_surface, enemy_transform, enemy_speed, enemy_identifier, enemy_tag


def create_input_player(world: esper.World):
    # Keyboard inputs
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()

    world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up, CInputCommand("PLAYER_UP", pygame.K_UP))
    world.add_component(input_down, CInputCommand("PLAYER_DOWN", pygame.K_DOWN))

    # Mouse inputs
    input_left_click = world.create_entity()
    world.add_component(input_left_click, CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT))


def create_explosion(world: esper.World, explosion_config, position):
    explosion_surface = pygame.image.load(explosion_config.image).convert_alpha()
    explosion_animation = CAnimation(explosion_config.animations)
    return create_sprite(world, explosion_surface, position, tag=CTagExplosion(), animation=explosion_animation, state=CPlayerState())
