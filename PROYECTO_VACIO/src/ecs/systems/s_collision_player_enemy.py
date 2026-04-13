import esper
import pygame

from src.create.prefab_creator import create_explosion_square
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.utils.config_loader import get_player_spawn_position_config

def system_collision_player_enemy(world: esper.World, player_entity: int) -> None:
    components = world.get_components(CSurface, CTransform, CTagEnemy)
    hunters = world.get_components(CSurface, CTransform, CTagHunter)
    
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    
    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)
    
    for enemy_entity, (c_s, c_t, _) in components + hunters:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        
        if ene_rect.colliderect(pl_rect):
            world.delete_entity(enemy_entity)
            
            
            pl_spawn = get_player_spawn_position_config()
            
            pl_t.pos.x = pl_spawn[0] - pl_s.area.width / 2
            pl_t.pos.y = pl_spawn[1] - pl_s.area.height / 2
            create_explosion_square(world, pygame.Vector2(ene_rect.center))