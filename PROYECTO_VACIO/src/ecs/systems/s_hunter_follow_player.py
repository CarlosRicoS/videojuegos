import esper
import pygame

from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.utils.config_loader import get_hunter_chase_distance, get_hunter_return_distance, get_hunter_velocity_chase, get_hunter_velocity_return


def system_hunter_follow_player(world: esper.World, player_entity: int):
    hunter_entities = world.get_components(CTransform, CVelocity, CHunterState, CTagHunter)
    player_transform: CTransform = world.component_for_entity(player_entity, CTransform)

    c_t: CTransform
    c_v: CVelocity
    c_hs: CHunterState
    RETURN_THRESHOLD = 2.0 
    

    for entity, (c_t, c_v, c_hs, _) in hunter_entities:
        
        # 1. Calculamos distancias base
        dist_player = (player_transform.pos - c_t.pos).magnitude()
        dir_origin = c_hs.origin - c_t.pos
        dist_origin = dir_origin.magnitude()

        # 2. Lógica basada en el ESTADO actual
        if c_hs.state == HunterState.IDLE:
            # Si estoy quieto, solo vigilo si el jugador entra en rango
            if dist_player <= get_hunter_chase_distance():
                _follow_player(c_t, c_v, player_transform)

        elif c_hs.state == HunterState.MOVE:
            # Si el cazador se aleja mucho, cambia a REGRESAR
            if dist_origin + RETURN_THRESHOLD >= get_hunter_return_distance():
                # if dist_player <= get_hunter_chase_distance():
                #     _return_to_origin(c_t, c_v, c_hs, dist_origin)
                # else:
                _return_to_origin(c_t, c_v, c_hs, dist_origin)
            else:
                # if dist_player <= get_hunter_chase_distance():
                _follow_player(c_t, c_v, player_transform)
                # else:
                #     _return_to_origin(c_t, c_v, c_hs, dist_origin)
            # elif dist_player > get_hunter_chase_distance():
            #     # Si el jugador se aleja del rango de persecución, regreso
            #     _return_to_origin(c_t, c_v, c_hs, dist_origin)
            # elif dist_player <= get_hunter_chase_distance() and dist_origin <= get_hunter_return_distance():
            #     # Perseguir activamente
            #     _follow_player(c_t, c_v, player_transform)

def _follow_player(c_t: CTransform, c_v: CVelocity, player_transform: CTransform):
    dir_player = (player_transform.pos - c_t.pos).normalize()
    c_v.vel = dir_player * get_hunter_velocity_chase()     
    
def _return_to_origin(c_t: CTransform, c_v: CVelocity, c_hs: CHunterState, dist_origin: float):
    dir_origin = (c_hs.origin - c_t.pos).normalize()
    c_v.vel = dir_origin * get_hunter_velocity_return()   
    STOP_THRESHOLD = 2.0 
    
    if dist_origin > STOP_THRESHOLD:
        c_v.vel = dir_origin.normalize() * get_hunter_velocity_return()
    else:
        # Llegada oficial
        c_v.vel = pygame.Vector2(0, 0)
        c_t.pos = c_hs.origin.copy()
        c_hs.state = HunterState.IDLE         