from typing import Callable

import pygame.event

import esper
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_input_command import CommandPhase


def system_input_player(world: esper.World, event: pygame.event.Event, do_action: Callable[[CInputCommand], None]):
    components = world.get_component(CInputCommand)

    for _, command in components:
        if event.type == pygame.KEYDOWN and event.key == command.key:
            command.phase = CommandPhase.START
            do_action(command)
        elif event.type == pygame.KEYUP and event.key == command.key:
            command.phase = CommandPhase.END
            do_action(command)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == command.key:
            command.phase = CommandPhase.START
            do_action(command)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == command.key:
            command.phase = CommandPhase.END
            do_action(command)
