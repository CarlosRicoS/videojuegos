import esper

from src.create.prefab_creator import _set_animation
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity
from src.utils.config_loader import get_animation_index_by_name


def system_player_state(world: esper.World):
    components = world.get_components(CVelocity, CAnimation, CPlayerState)
    
    for _, (c_vel, c_anim, c_ps) in components:
        if c_ps.state == PlayerState.IDLE:
            _do_idle_state(c_vel, c_anim, c_ps)
        elif c_ps.state == PlayerState.MOVE:
            _do_move_state(c_vel, c_anim, c_ps)

            
def _do_idle_state(c_vel: CVelocity, c_anim: CAnimation, c_ps: CPlayerState):
    _set_animation(c_anim, get_animation_index_by_name(PlayerState.IDLE.name, c_anim.animation_list))
    if c_vel.vel.magnitude_squared() > 0:
        c_ps.state = PlayerState.MOVE
    
def _do_move_state(c_vel: CVelocity, c_anim: CAnimation, c_ps: CPlayerState):   
    _set_animation(c_anim, get_animation_index_by_name(PlayerState.MOVE.name, c_anim.animation_list))
    if c_vel.vel.magnitude_squared() <= 0:
        c_ps.state = PlayerState.IDLE
    