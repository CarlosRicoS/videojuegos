import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_mine import CTagMine
from src.engine.service_locator import ServiceLocator
from src.utils.config_loader import get_player_sound


def system_screen_bounce(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy)
    mines = world.get_components(CTransform, CVelocity, CSurface, CTagMine)
    
    c_t: CTransform
    c_v: CVelocity
    c_s: CSurface
    
    for entity, (c_t, c_v, c_s, c_e) in components + mines:
        obj_rect = c_s.surface.get_rect(topleft=c_t.pos)
        
        if obj_rect.right > screen_rect.width or obj_rect.left < 0:
            c_v.vel.x *= -1
            obj_rect.clamp_ip(screen_rect)
            c_t.pos.x = obj_rect.x
            
        if obj_rect.bottom > screen_rect.height or obj_rect.top < 0:
            c_v.vel.y *= -1          
            obj_rect.clamp_ip(screen_rect)
            c_t.pos.y = obj_rect.y