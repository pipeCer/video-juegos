import random

import pygame

import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_input_command import CommandPhase
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_tag_bullet import CTagBullet
from src.ecs.components.c_transform import CTransform
from src.ecs.systems.s_bullet_enemy_collision import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_movement import system_movement_bullet
from src.ecs.systems.s_movement import system_movement_player
from src.ecs.systems.s_rendering import system_render_square
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.engine.prefabs import create_bullet_square
from src.engine.prefabs import create_enemy
from src.engine.prefabs import create_input_player
from src.engine.prefabs import create_player
from src.utils import read_json
from src.utils import validate_position


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.window = self.window_config
        self._init_window()
        self.player = self.player_config
        self.bullet = self.bullet_config
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.fps = self.window.framerate  # frames per second
        self.delta_time = 0
        self.current_time = 0
        self.current_index = 0
        self.ecs_world = esper.World()
        self.show_message = False

    @property
    def window_config(self):
        return self.read_config("window")

    @property
    def enemies_config(self):
        return self.read_config("enemies")

    @property
    def level_config(self):
        return self.read_config("level")

    @property
    def player_config(self):
        return self.read_config("player")

    @property
    def bullet_config(self):
        return self.read_config("bullet")

    @staticmethod
    def read_config(config_name):
        return read_json(config_name)

    def _init_window(self):
        pygame.display.set_caption(self.window.title)
        self.screen = pygame.display.set_mode((self.window.size.w, self.window.size.h), pygame.SCALED)

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self._player_entity = create_player(self.ecs_world, self.player, self.level_config.player_spawn)
        self._player_speed = self.ecs_world.component_for_entity(self._player_entity, CSpeed)
        self._player_transform = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        entity = self.ecs_world.create_entity()
        enemies = self.enemies_config

        populated_enemies = []

        for config in self.level_config.enemy_spawn_events:
            try:
                current_enemy = getattr(enemies, config["enemy_type"])
                current_enemy_size = pygame.Vector2(current_enemy.size.x, current_enemy.size.y)

                speed_direction = random.choice([-1, 1])
                scalar_enemy_speed = random.randint(current_enemy.velocity_min, current_enemy.velocity_max) * speed_direction
                current_enemy_speed = pygame.Vector2(scalar_enemy_speed, scalar_enemy_speed)

                current_enemy_color = pygame.Color(current_enemy.color.r, current_enemy.color.g, current_enemy.color.b)
                x, y = validate_position(
                    x=config["position"]["x"],
                    y=config["position"]["y"],
                    bounds_size=(self.window.size.w, self.window.size.h),
                    offset=(current_enemy_size.x, current_enemy_size.y),
                )
                current_enemy_position = pygame.Vector2(x, y)

                populated_enemies.append(create_enemy(current_enemy_size, current_enemy_color, current_enemy_position, current_enemy_speed, config["enemy_type"], config["time"]))
            except AttributeError:
                print(f"Enemy type {config['enemy_type']} not found in level config")

        if not populated_enemies:
            self.show_message = True

        current_enemies = CEnemySpawner(populated_enemies)
        self.ecs_world.add_component(entity, current_enemies)

        create_input_player(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.fps)
        self.delta_time = self.clock.get_time() / 1000  # convert to seconds

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_movement_player(self.ecs_world, self.delta_time, self.screen)
        system_movement_bullet(self.ecs_world, self.delta_time, self.screen)
        system_screen_bounce(self.ecs_world, self.screen)
        system_collision_player_enemy(self.ecs_world, self._player_entity, self.level_config.player_spawn)
        system_collision_bullet_enemy(self.ecs_world)
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        if self.show_message:
            self._write_text(
                text="No enemies found in level config",
                font=pygame.font.SysFont("Arial", 24),
                color=(255, 255, 255),
                x=self.window.size.w // 2 - 200,
                y=self.window.size.h // 2 - 50,
            )
        else:
            self.current_time += self.delta_time
            self.screen.fill((self.window.bg_color.r, self.window.bg_color.g, self.window.bg_color.b))
            system_enemy_spawner(self.ecs_world, self.current_time, self.screen)
            system_render_square(self.ecs_world, self.screen)

        pygame.display.flip()

    def _write_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        input_speed = self.player.input_velocity
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_speed.speed.x -= input_speed
            elif c_input.phase == CommandPhase.END:
                self._player_speed.speed.x += input_speed
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_speed.speed.x += input_speed
            elif c_input.phase == CommandPhase.END:
                self._player_speed.speed.x -= input_speed
        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self._player_speed.speed.y -= input_speed
            elif c_input.phase == CommandPhase.END:
                self._player_speed.speed.y += input_speed
        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self._player_speed.speed.y += input_speed
            elif c_input.phase == CommandPhase.END:
                self._player_speed.speed.y -= input_speed
        if c_input.name == "PLAYER_FIRE":
            if c_input.phase == CommandPhase.START:
                components = self.ecs_world.get_components(CTagBullet)
                # This will depend on the logic of the game
                if len(components) < self.level_config.player_spawn.max_bullets:
                    create_bullet_square(self.ecs_world, self.bullet, self._player_transform.position, self.player.size)
            elif c_input.phase == CommandPhase.END:
                pass
