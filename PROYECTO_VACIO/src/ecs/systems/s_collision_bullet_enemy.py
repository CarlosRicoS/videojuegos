import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.utils.config_loader import get_player_spawn_position_config

def system_collision_bullet_enemy(world: esper.World, player_entity: int) -> None:
    enemies = world.get_components(CSurface, CTransform, CTagEnemy)
    bullets = world.get_components(CSurface, CTransform, CTagBullet)
    
    for enemy_entity, (c_s, c_t, _) in enemies:
        for bullet_entity, (b_s, b_t, _) in bullets:
            bul_rect = b_s.surface.get_rect(topleft=b_t.pos)
            ene_rect = c_s.surface.get_rect(topleft=c_t.pos)
            if ene_rect.colliderect(bul_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                