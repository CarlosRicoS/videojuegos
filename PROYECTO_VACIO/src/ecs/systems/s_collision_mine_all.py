import esper
import pygame

from src.create.prefab_creator import create_explosion_square, create_player_lifes_indicator
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.ecs.components.tags.c_tag_mine import CTagMine
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.utils.config_loader import get_player_spawn_position_config


def system_collision_mine_all(world: esper.World, screen: pygame.Surface):
    enemies = world.get_components(CSurface, CTransform, CTagEnemy)
    hunters = world.get_components(CSurface, CTransform, CTagHunter)
    player = world.get_components(CSurface, CTransform, CTagPlayer)
    
    affected = enemies + hunters + player
    
    mines = world.get_components(CSurface, CTransform, CTagMine)
    
    for affected_entity, (c_s, c_t, _) in affected:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for mine_entity, (m_s, m_t, _) in mines:
            mine_rect = CSurface.get_area_relative(m_s.area, m_t.pos)
            
            if ene_rect.colliderect(mine_rect):
                if world.has_component(affected_entity, CTagPlayer):
                    pl_st = world.component_for_entity(affected_entity, CPlayerState)
                    pl_spawn = get_player_spawn_position_config()
                    c_t.pos.x = pl_spawn[0] - c_s.area.width / 2
                    c_t.pos.y = pl_spawn[1] - c_s.area.height / 2
                    world.delete_entity(mine_entity)
                    create_explosion_square(world, pygame.Vector2(ene_rect.center))
                    pl_st.lifes -= 1
                    create_player_lifes_indicator(world, screen, pl_st.lifes)
                else:                     
                    world.delete_entity(mine_entity)
                    world.delete_entity(affected_entity)
                    create_explosion_square(world, pygame.Vector2(ene_rect.center))
                