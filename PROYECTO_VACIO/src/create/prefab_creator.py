import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.utils.config_loader import LevelEventState, get_bg_color, get_window_size, get_window_title

def create_enemy_spawner(world: esper.World, spawn_events: list[LevelEventState]) -> None:
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(spawn_events=spawn_events))
    
def create_window():
    screen = pygame.display.set_mode(get_window_size(), pygame.SCALED)
    pygame.display.set_caption(get_window_title())
    return screen

def fill_window(screen: pygame.Surface):
    screen.fill(get_bg_color())