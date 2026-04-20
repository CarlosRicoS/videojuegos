import random

import esper
import pygame

from src.create.prefab_creator import create_special_bullet_square
from src.ecs.components.c_event_time import CEventTime
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_expired_mines import CTagExpiredMines
from src.ecs.components.tags.c_tag_mine import CTagMine
from src.ecs.components.tags.c_tag_special_power_event import CTagSpecialPowerEvent
from src.engine.service_locator import ServiceLocator
from src.utils.config_loader import get_level_mine_limit, get_special_bullet_texture, get_special_bullet_velocity

def system_special_power(world: esper.World, event_time: float) -> None:
    
    is_loading = len(world.get_component(CTagSpecialPowerEvent)) > 0
    
    if(is_loading):
        return
    
    bullet_components = world.get_components(CSurface, CTagBullet)
    mine_texture = ServiceLocator.images_service.get(get_special_bullet_texture())
    mine_size = mine_texture.get_size()
    
    mine_direcitons = [
        pygame.Vector2(0.5, 0.5),
        pygame.Vector2(-0.5, 0.5),
        pygame.Vector2(0.5, -0.5),
        pygame.Vector2(-0.5, -0.5)
    ]
    
    c_s: CSurface
    event = world.create_entity(CEventTime(event_time))
    world.add_component(event, CTagSpecialPowerEvent())
    for bullet_entity, (c_s, _) in bullet_components:
        bullet_pos = world.component_for_entity(bullet_entity, CTransform).pos
        bullet_rect = c_s.get_area_relative(c_s.area, bullet_pos)
        
        for direction in mine_direcitons:
            mines = world.get_component(CTagMine) 
            if len(mines) >= get_level_mine_limit():
                return
        
            create_special_bullet_square(
                world, 
                position=pygame.Vector2(bullet_rect.centerx - mine_size[0] / 2, bullet_rect.centery - mine_size[1] / 2),
                texture=mine_texture,
                velocity=pygame.Vector2(direction.normalize() * get_special_bullet_velocity())
            )
        
        world.delete_entity(bullet_entity)
        