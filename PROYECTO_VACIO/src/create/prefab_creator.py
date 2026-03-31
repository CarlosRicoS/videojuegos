import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.utils.config_loader import LevelEventState, get_bg_color, get_player_color, get_player_size, get_window_size, get_window_title

def create_square(world: esper.World, 
        size: pygame.Vector2, 
        position: pygame.Vector2, 
        color: pygame.Color, 
        velocity: pygame.Vector2 = pygame.Vector2(0, 0)) -> int:
    
    entity = world.create_entity()
    world.add_component(entity, CSurface(size, color))
    world.add_component(entity, CTransform(position))
    world.add_component(entity, CVelocity(velocity))
    return entity


def create_enemy_spawner(world: esper.World, spawn_events: list[LevelEventState]) -> None:
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(spawn_events=spawn_events))
    
def create_window():
    screen = pygame.display.set_mode(get_window_size(), pygame.SCALED)
    pygame.display.set_caption(get_window_title())
    return screen

def fill_window(screen: pygame.Surface):
    screen.fill(get_bg_color())

def create_enemy_square(world: esper.World, 
        size: pygame.Vector2, 
        position: pygame.Vector2, 
        color: pygame.Color, 
        velocity: pygame.Vector2) -> int:
    enemy_entity = create_square(
            world,
            size,
            position,
            color,
            velocity
        )
    world.add_component(enemy_entity, CTagEnemy())
    return enemy_entity
    
def create_player_square(world: esper.World, 
        spawn_position_config: tuple[int, int]) -> int:
    size=pygame.Vector2(get_player_size())
    position=pygame.Vector2(
        spawn_position_config[0] - size.x / 2, 
        spawn_position_config[1] - size.y / 2)
    player_entity = create_square(
        world,
        size=size,
        position=position,
        color=pygame.Color(get_player_color())
    )
    world.add_component(player_entity, CTagPlayer())
    return player_entity

def create_bullet_square(world: esper.World, 
        size: pygame.Vector2, 
        position: pygame.Vector2, 
        color: pygame.Color, 
        velocity: pygame.Vector2
        ) -> int:
    bullet_entity = create_square(
            world,
            size,
            position,
            color,
            velocity
        )
    world.add_component(bullet_entity, CTagBullet())
    return bullet_entity

def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_shoot = world.create_entity()
    world.add_component(input_left, CInputCommand('PLAYER_LEFT', pygame.K_LEFT))
    world.add_component(input_right, CInputCommand('PLAYER_RIGHT', pygame.K_RIGHT))
    world.add_component(input_up, CInputCommand('PLAYER_UP', pygame.K_UP))
    world.add_component(input_down, CInputCommand('PLAYER_DOWN', pygame.K_DOWN))
    world.add_component(input_shoot, CInputCommand('PLAYER_FIRE', pygame.BUTTON_LEFT))