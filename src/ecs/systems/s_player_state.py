import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_player_state import PlayerState
from src.ecs.components.c_speed import CSpeed


def system_player_state(world: esper.World):
    components = world.get_components(CSpeed, CAnimation, CPlayerState)
    for _, (c_speed, c_animation, c_player_state) in components:
        if c_player_state.state == PlayerState.IDLE:
            _do_idle_state(c_speed, c_animation, c_player_state)
        elif c_player_state.state == PlayerState.MOVE:
            _do_move_state(c_speed, c_animation, c_player_state)


def _do_idle_state(c_speed, c_animation, c_player_state):
    _set_animation(c_animation, 1)
    if c_speed.speed.magnitude_squared() > 0:
        c_player_state.state = PlayerState.MOVE


def _do_move_state(c_speed, c_animation, c_player_state):
    _set_animation(c_animation, 0)
    if c_speed.speed.magnitude_squared() == 0:
        c_player_state.state = PlayerState.IDLE


def _set_animation(c_animation, num_animation):
    if c_animation.current_animation == num_animation:
        return
    c_animation.current_animation = num_animation
    c_animation.current_animation_time = 0
    c_animation.current_frame = c_animation.animation_list[c_animation.current_animation].start
