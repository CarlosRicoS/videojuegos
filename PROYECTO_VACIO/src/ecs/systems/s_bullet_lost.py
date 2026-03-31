import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_bullet_lost(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagBullet)
    
    c_t: CTransform
    c_s: CSurface
    
    for entity, (c_t, c_s, c_b) in components:
        obj_rect = c_s.surface.get_rect(topleft=c_t.pos)
        
        if not screen_rect.colliderect(obj_rect):
            world.delete_entity(entity)