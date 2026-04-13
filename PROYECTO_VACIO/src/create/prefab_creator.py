import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.utils.config_loader import LevelEventState, get_bg_color, get_explosion_animation, get_explosion_frames_count, get_explosion_texture, get_hunter_animations, get_hunter_animations, get_player_animations, get_player_animations, get_player_frames_count, get_player_frames_count, get_player_texture, get_window_size, get_window_title

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

def create_sprite(world: esper.World, 
        position: pygame.Vector2, 
        surface: pygame.Surface,
        velocity: pygame.Vector2 = pygame.Vector2(0, 0)) -> int:
    
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(position))
    world.add_component(sprite_entity, CVelocity(velocity))
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity

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
        texture: pygame.Surface,                        
        position: pygame.Vector2, 
        velocity: pygame.Vector2) -> int:
    enemy_entity = create_sprite(
            world,
            position,
            texture,
            velocity
        )
    world.add_component(enemy_entity, CTagEnemy())
    return enemy_entity
    
def create_player_square(world: esper.World, 
        spawn_position_config: tuple[int, int]) -> int:
    player_sprite = pygame.image.load(get_player_texture()).convert_alpha()
    size = player_sprite.get_size()
    size = (size[0] / get_player_frames_count(), size[1] / get_player_frames_count())
    position=pygame.Vector2(
        spawn_position_config[0] - size[0] / 2, 
        spawn_position_config[1] - size[1] / 2)
    player_entity = create_sprite(
        world,
        position=position,
        surface=player_sprite
    )
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity, CAnimation(get_player_animations()))
    world.add_component(player_entity, CPlayerState())
    return player_entity

def create_bullet_square(world: esper.World, 
        texture: pygame.Surface,
        position: pygame.Vector2, 
        velocity: pygame.Vector2
        ) -> int:
    bullet_entity = create_sprite(
            world,
            position,
            texture,
            velocity
        )
    world.add_component(bullet_entity, CTagBullet())
    return bullet_entity

def create_explosion_square(world: esper.World,
        position: pygame.Vector2) -> int:
    explosion_sprite = pygame.image.load(get_explosion_texture()).convert_alpha()
    size = explosion_sprite.get_size()
    size = (size[0] / get_explosion_frames_count(), size[1] / get_explosion_frames_count())
    explosion_position=pygame.Vector2(
        position[0] - size[0] / 2, 
        position[1] - size[1] / 2)
    explosion_entity = create_sprite(
            world,
            position=explosion_position,
            surface=explosion_sprite,
            velocity=pygame.Vector2(0, 0)
        )
    world.add_component(explosion_entity, CAnimation(get_explosion_animation()))
    world.add_component(explosion_entity, CTagExplosion())
    return explosion_entity

def create_hunter_square(world: esper.World, 
        texture: pygame.Surface,                        
        position: pygame.Vector2) -> int:
    hunter_entity = create_sprite(
            world,
            position,
            texture,
            velocity=pygame.Vector2(0, 0)
        )
    world.add_component(hunter_entity, CAnimation(get_hunter_animations()))
    world.add_component(hunter_entity, CTagHunter())
    world.add_component(hunter_entity, CHunterState(position.copy()))
    
    return hunter_entity

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
    
def _set_animation(c_anim: CAnimation, anim_id: int):
    if c_anim.curr_anim == anim_id:
        return
    c_anim.curr_anim = anim_id
    c_anim.current_animation_time = 0
    c_anim.current_frame = c_anim.current_frame = c_anim.animation_list[c_anim.curr_anim].start
    