import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_is_hidden import CTagIsHidden

def system_rendering(world: esper.World, screen: pygame.Surface):
    components = world.get_components(CTransform, CSurface)
    
    c_t: CTransform
    c_s: CSurface
    
    for entity, (c_t, c_s) in components:
        if world.has_component(entity, CTagIsHidden):
            continue
        screen.blit(c_s.surface, c_t.pos, area=c_s.area)    