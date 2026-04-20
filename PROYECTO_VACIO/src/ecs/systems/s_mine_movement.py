import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_mine import CTagMine
from src.ecs.components.tags.c_tag_placed_mine import CTagPlacedMine
from src.engine.service_locator import ServiceLocator
from src.utils.config_loader import get_special_bullet_radius, get_special_bullet_sound


def system_mine_movement(world: esper.World):
    components = world.get_components(CVelocity, CTransform, CTagMine)

    c_v = CVelocity
    c_t = CTransform
    
    for mine_entity, (c_v, c_t, _) in components:
        mine_distance = pygame.Vector2(c_t.pos.x - c_t.origin.x, c_t.pos.y - c_t.origin.y).length()
        
        if mine_distance >= get_special_bullet_radius():  
            c_v.vel = pygame.Vector2(0, 0)
            if(world.has_component(mine_entity, CTagPlacedMine) == False):
                world.add_component(mine_entity, CTagPlacedMine())
                ServiceLocator.sounds_service.play(get_special_bullet_sound())
    