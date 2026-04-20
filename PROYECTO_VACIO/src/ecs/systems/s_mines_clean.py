import esper
import pygame

from src.create.prefab_creator import create_explosion_square
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_expired_mines import CTagExpiredMines


def system_mines_clean(world: esper.World):
    mine_components = world.get_components(CSurface, CTransform, CTagExpiredMines)
    
    c_s: CSurface
    c_t: CTransform
    
    for mine_entity, (c_s, c_t, _) in mine_components:
        world.delete_entity(mine_entity)
        bullet_rect = c_s.get_area_relative(c_s.area, c_t.pos)
        create_explosion_square(world, pygame.Vector2(bullet_rect.center))