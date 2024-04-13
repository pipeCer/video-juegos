import uuid

import pygame
from pygame import Color
from pygame import Vector2

import esper
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_tag_enemy import CTagEnemy
from src.ecs.components.c_tag_player import CTagPlayer
from src.ecs.components.c_transform import CTransform


def create_square(world, size, position, color, speed, tag):
    entity = world.create_entity()
    world.add_component(entity, CSurface(size, color))
    world.add_component(entity, CTransform(position))
    world.add_component(entity, CSpeed(speed))
    world.add_component(entity, tag)
    return entity


def create_bullet_square(world: esper.World, bullet, player_position, player_size):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    direction_vector = pygame.Vector2(mouse_x - player_position.x, mouse_y - player_position.y)
    direction_vector.normalize_ip()
    bullet_velocity = direction_vector * bullet.velocity
    bullet_entity = create_square(
        world=world,
        size=pygame.Vector2(bullet.size.x, bullet.size.y),
        position=pygame.Vector2(player_position.x + player_size.x / 2, player_position.y + player_size.y / 2),
        speed=bullet_velocity,
        color=pygame.Color(bullet.color.r, bullet.color.g, bullet.color.b),
        tag=CTagBullet(),
    )
    world.add_component(bullet_entity, CTagBullet())


def create_player(world, player_config, player_spawn):
    player_size = Vector2(player_config.size.x, player_config.size.y)
    player_color = Color(player_config.color.r, player_config.color.g, player_config.color.b)
    player_position = Vector2(player_spawn.position.x, player_spawn.position.y)
    player_speed = Vector2(0, 0)

    return create_square(world, player_size, player_position, player_color, player_speed, CTagPlayer())


def create_enemy(enemy_size: Vector2, enemy_color: Color, enemy_position: Vector2, enemy_speed: Vector2, enemy_identifier: str, spawn_time: int):
    enemy_surface = CSurface(enemy_size, enemy_color)
    enemy_transform = CTransform(enemy_position)
    enemy_speed = CSpeed(enemy_speed)
    enemy_identifier = CMetadata(f"{enemy_identifier}_{uuid.uuid4()}", spawn_time)
    enemy_tag = CTagEnemy()
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
