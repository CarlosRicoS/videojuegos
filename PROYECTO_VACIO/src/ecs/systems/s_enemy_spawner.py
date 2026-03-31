import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.utils.config_loader import LevelEventState, get_enemy_by_name, get_enemy_color, get_enemy_size, get_enemy_velocity_range, get_event_enemy_type, get_event_position, get_event_time, set_event_triggered

def system_enemy_spawner(world: esper.World, elapsed_time: float):
    enemy_spawner: CEnemySpawner = world.get_component(CEnemySpawner)[0][1] 

    next_event = next(
        (event for event in enemy_spawner.spawn_events if not next(iter(event.values()))),
        None,
    )
    if next_event is None:
        return

    if elapsed_time >= get_event_time(next_event):
        enemy_type = get_event_enemy_type(next_event)
        enemy = get_enemy_by_name(enemy_type)
        enemy_entity = world.create_entity()
        world.add_component(enemy_entity, 
            CSurface(
                size=pygame.Vector2(get_enemy_size(enemy)), 
                color=pygame.Color(get_enemy_color(enemy)),
            )
        )
        world.add_component(enemy_entity, 
            CTransform(
                pos=pygame.Vector2(get_event_position(next_event))
            )
        )
        world.add_component(enemy_entity, 
            CVelocity(
                vel=pygame.Vector2(get_enemy_velocity_range(enemy))
            )
        )
        
        set_event_triggered(next_event)