import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity


def system_player_state(world: esper.World):
    components = world.get_components(CVelocity, CAnimation, CPlayerState)
    
    for _, (c_vel, c_anim, c_ps) in components:
        if c_ps.state == PlayerState.IDLE:
            _do_idle_state(c_vel, c_anim, c_ps)
        elif c_ps.state == PlayerState.MOVE:
            _do_move_state(c_vel, c_anim, c_ps)

            
def _do_idle_state(c_vel: CVelocity, c_anim: CAnimation, c_ps: CPlayerState):
    _set_animation(c_anim, PlayerState.IDLE.value)
    if c_vel.vel.magnitude_squared() > 0:
        c_ps.state = PlayerState.MOVE
    
def _do_move_state(c_vel: CVelocity, c_anim: CAnimation, c_ps: CPlayerState):   
    _set_animation(c_anim, PlayerState.MOVE.value)
    if c_vel.vel.magnitude_squared() <= 0:
        c_ps.state = PlayerState.IDLE
    
def _set_animation(c_anim: CAnimation, anim_id: int):
    if c_anim.curr_anim == anim_id:
        return
    c_anim.curr_anim = anim_id
    c_anim.current_animation_time = 0
    c_anim.current_frame = c_anim.current_frame = c_anim.animation_list[c_anim.curr_anim].start
    