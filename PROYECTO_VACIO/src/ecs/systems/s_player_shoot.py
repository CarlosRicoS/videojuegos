import esper
import pygame

from src.create.prefab_creator import create_bullet_square
from src.ecs.components.c_input_command import CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator
from src.utils.config_loader import get_bullet_texture, get_bullet_velocity, get_level_bullet_limit


def system_player_shoot(world: esper.World, 
        bullet_direction: pygame.Vector2,
        player_entity: int):
    bullets = world.get_component(CTagBullet)
    
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    
    player_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)
    
    if len(bullets) < get_level_bullet_limit():
        direction = bullet_direction - player_rect.center
    
        bullet_texture = ServiceLocator.images_service.get(get_bullet_texture())
        bullet_size = bullet_texture.get_size()
        
        create_bullet_square(
            world, 
            position=pygame.Vector2(player_rect.center[0] - bullet_size[0] / 2, player_rect.center[1] - bullet_size[1] / 2),
            texture=bullet_texture,
            velocity=pygame.Vector2(direction.normalize() * get_bullet_velocity())
        )
        