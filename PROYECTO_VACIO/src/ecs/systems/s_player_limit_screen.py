import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_player_limit_screen(world: esper.World, 
        screen: pygame.Surface,
        player_entity: int):
    screen_rect = screen.get_rect()
    
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    
    player_rect = pl_s.surface.get_rect(topleft=pl_t.pos)
    
    if player_rect.right > screen_rect.width or player_rect.left < 0:
        player_rect.clamp_ip(screen_rect)
        pl_t.pos.x = player_rect.x
        
    if player_rect.bottom > screen_rect.height or player_rect.top < 0:
        player_rect.clamp_ip(screen_rect)
        pl_t.pos.y = player_rect.y
            