import esper

from src.create.prefab_creator import _set_animation
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.engine.service_locator import ServiceLocator
from src.utils.config_loader import get_animation_index_by_name, get_hunter_chase_distance, get_hunter_chase_sound, get_hunter_return_distance, get_hunter_velocity_chase, get_hunter_velocity_return


def system_hunter_state(world: esper.World):
    hunter_entities = world.get_components(CVelocity, CAnimation, CHunterState, CTagHunter)

    c_v: CVelocity
    c_hs: CHunterState
    
    for _, (c_v, c_a, c_hs, _) in hunter_entities:
    
        if c_hs.state == HunterState.IDLE:
            _do_idle_state(c_v, c_a, c_hs)
        elif c_hs.state == HunterState.MOVE:
            _do_move_state(c_v, c_a, c_hs)
        
        
def _do_idle_state(c_vel: CVelocity, c_anim: CAnimation, c_hs: CHunterState):
    _set_animation(c_anim, get_animation_index_by_name(HunterState.IDLE.name, c_anim.animation_list))
    if c_vel.vel.magnitude_squared() > 0:
        c_hs.state = HunterState.MOVE
        ServiceLocator.sounds_service.play(get_hunter_chase_sound() )
        
def _do_move_state(c_vel: CVelocity, c_anim: CAnimation, c_hs: CHunterState):   
    _set_animation(c_anim, get_animation_index_by_name(HunterState.MOVE.name, c_anim.animation_list))
    if c_vel.vel.magnitude_squared() <= 0:
        c_hs.state = HunterState.IDLE        
        
    