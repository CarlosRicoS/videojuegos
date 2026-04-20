import esper
import pygame

from src.create.prefab_creator import create_explosion_square
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_hunter import CTagHunter

def system_collision_bullet_enemy(world: esper.World, player_entity: int) -> None:
    enemies = world.get_components(CSurface, CTransform, CTagEnemy)
    hunters = world.get_components(CSurface, CTransform, CTagHunter)
    bullets = world.get_components(CSurface, CTransform, CTagBullet)
    
    for enemy_entity, (c_s, c_t, _) in enemies + hunters:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        
        for bullet_entity, (b_s, b_t, _) in bullets:
            bul_rect = CSurface.get_area_relative(b_s.area, b_t.pos)
            
            if ene_rect.colliderect(bul_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                
                create_explosion_square(world, pygame.Vector2(ene_rect.center))
                