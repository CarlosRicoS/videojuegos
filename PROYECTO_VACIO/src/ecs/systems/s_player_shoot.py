import esper
import pygame

from src.create.prefab_creator import create_bullet_square
from src.ecs.components.c_input_command import CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.utils.config_loader import get_bullet_color, get_bullet_size, get_bullet_velocity, get_level_bullet_limit


def system_player_shoot(world: esper.World, 
        bullet_direction: pygame.Vector2,
        player_entity: int):
    bullets = world.get_component(CTagBullet)
    
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    
    player_rect = pl_s.surface.get_rect(topleft=pl_t.pos)
    
    if len(bullets) < get_level_bullet_limit():
        direction = bullet_direction - player_rect.center
        
        create_bullet_square(
            world, 
            size=pygame.Vector2(get_bullet_size()),
            position=pygame.Vector2(player_rect.center),
            color=pygame.Color(get_bullet_color()),
            velocity=pygame.Vector2(direction.normalize() * get_bullet_velocity())
        )
        