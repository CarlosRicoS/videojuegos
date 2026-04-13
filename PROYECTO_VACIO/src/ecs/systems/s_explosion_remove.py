import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_explosion_remove(world: esper.World) -> None:
    explosions = world.get_components(CTagExplosion, CAnimation)
    
    for entity, (c_e, c_a) in explosions:
        if c_a.current_frame >= c_a.animation_list[c_a.curr_anim].end:
            world.delete_entity(entity)