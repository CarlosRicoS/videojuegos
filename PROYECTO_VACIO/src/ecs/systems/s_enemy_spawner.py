import esper
import pygame

from src.create.prefab_creator import create_enemy_square, create_square
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.utils.config_loader import LevelEventState, get_enemy_by_name, get_enemy_texture, get_enemy_velocity_range, get_event_enemy_type, get_event_position, get_event_time, set_event_triggered

def system_enemy_spawner(world: esper.World, elapsed_time: float):
    enemy_spawner: CEnemySpawner
    _, enemy_spawner = next(iter(world.get_component(CEnemySpawner)), (None, None))
    
    next_event: LevelEventState

    for next_event in enemy_spawner.spawn_events:
    
        event, is_triggered = next(iter(next_event.items()))
        
        if next_event is None:
            break
        
        if is_triggered is True:
            continue

        if elapsed_time >= get_event_time(next_event):
            enemy_type = get_event_enemy_type(next_event)
            enemy = get_enemy_by_name(enemy_type)
            create_enemy_square(
                world,
                texture=pygame.image.load(get_enemy_texture(enemy_type)).convert_alpha(),
                position=pygame.Vector2(get_event_position(next_event)),
                velocity=pygame.Vector2(get_enemy_velocity_range(enemy))
            )
            set_event_triggered(next_event)