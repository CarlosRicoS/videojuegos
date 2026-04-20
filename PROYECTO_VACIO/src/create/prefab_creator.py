import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_game_state import CGameState
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_hunter import CTagHunter
from src.ecs.components.tags.c_tag_is_hidden import CTagIsHidden
from src.ecs.components.tags.c_tag_lifes_label import CTagLifesLabel
from src.ecs.components.tags.c_tag_load_text import CTagLoadText
from src.ecs.components.tags.c_tag_mine import CTagMine
from src.ecs.components.tags.c_tag_pause_text import CTagPauseText
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.engine.service_locator import ServiceLocator
from src.utils.config_loader import LevelEventState, get_bg_color, get_bullet_sound, get_explosion_animation, get_explosion_frames_count, get_explosion_sound, get_explosion_sound, get_explosion_texture, get_hunter_animations, get_hunter_animations, get_interface_end_game_color, get_interface_end_game_size, get_interface_font, get_interface_instructions_color, get_interface_instructions_size, get_interface_instructions_text, get_interface_load_color, get_interface_load_size, get_interface_lose_text, get_interface_pause_color, get_interface_pause_size, get_interface_pause_text, get_interface_player_lifes_color, get_interface_player_lifes_color, get_interface_player_lifes_size, get_interface_title_color, get_interface_title_size, get_interface_title_text, get_interface_win_text, get_player_animations, get_player_animations, get_player_frames_count, get_player_frames_count, get_player_lose_sound, get_player_texture, get_player_win_sound, get_window_size, get_window_title

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
        velocity: pygame.Vector2 = pygame.Vector2(0, 0),
        keep_origin: bool = False
    ) -> int:
    
    sprite_entity = world.create_entity()
    if keep_origin is True:
        world.add_component(sprite_entity, CTransform.from_original_position(position))
    else:
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
    player_sprite = ServiceLocator.images_service.get(get_player_texture())
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
    ServiceLocator.sounds_service.play(get_bullet_sound())
    return bullet_entity

def create_special_bullet_square(world: esper.World,
                                 texture: pygame.Surface,
                                 position: pygame.Vector2,
                                 velocity: pygame.Vector2) -> int:
    bullet_entity = create_sprite(
            world,
            position,
            texture,
            velocity,
            keep_origin=True
        )
    world.add_component(bullet_entity, CTagMine())
    return bullet_entity

def create_end_game_message(world: esper.World, screen: pygame.Surface, is_winner: bool):
    font: pygame.font.Font = ServiceLocator.texts_service.get_font(
        get_interface_font())
    font.set_point_size(get_interface_end_game_size())
    text_entity = world.create_entity()
    c_surface = CSurface.from_text(
        get_interface_win_text() if is_winner else get_interface_lose_text(),
        font,
        pygame.Color(get_interface_end_game_color())
    )
    text_center = c_surface.surface.get_rect()
    text_center.center = screen.get_rect().center
    c_transform = CTransform(pygame.Vector2(text_center.x, text_center.y))

    world.add_component(text_entity, c_surface)
    world.add_component(text_entity, c_transform)
    
    ServiceLocator.sounds_service.play(get_player_win_sound() if is_winner else get_player_lose_sound())

def create_explosion_square(world: esper.World,
        position: pygame.Vector2) -> int:
    explosion_sprite = ServiceLocator.images_service.get(get_explosion_texture())
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
    ServiceLocator.sounds_service.play(get_explosion_sound())
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

def create_game_state(world: esper.World):
    game_state_entity = world.create_entity()
    world.add_component(game_state_entity, CGameState())
    return game_state_entity

def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_pause = world.create_entity()
    input_shoot = world.create_entity()
    input_special = world.create_entity()
    world.add_component(input_left, CInputCommand('PLAYER_LEFT', pygame.K_LEFT))
    world.add_component(input_right, CInputCommand('PLAYER_RIGHT', pygame.K_RIGHT))
    world.add_component(input_up, CInputCommand('PLAYER_UP', pygame.K_UP))
    world.add_component(input_down, CInputCommand('PLAYER_DOWN', pygame.K_DOWN))
    world.add_component(input_pause, CInputCommand('PLAYER_PAUSE', pygame.K_p))
    world.add_component(input_shoot, CInputCommand('PLAYER_FIRE', pygame.BUTTON_LEFT))
    world.add_component(input_special, CInputCommand('PLAYER_SPECIAL', pygame.BUTTON_RIGHT))
    
    
def create_title_text(world: esper.World, screen: pygame.Surface):
    font: pygame.font.Font = ServiceLocator.texts_service.get_font(
        get_interface_font())
    font.set_point_size(get_interface_title_size())
    text_entity = world.create_entity()
    c_surface = CSurface.from_text(
        get_interface_title_text(),
        font,
        pygame.Color(get_interface_title_color())
    )
    text_center = c_surface.surface.get_rect()
    text_center.topleft = screen.get_rect().topleft
    c_transform = CTransform(pygame.Vector2(text_center.x, text_center.y))

    world.add_component(text_entity, c_surface)
    world.add_component(text_entity, c_transform)

def create_pause_text(world: esper.World, screen: pygame.Surface):
    font: pygame.font.Font = ServiceLocator.texts_service.get_font(
        get_interface_font())
    font.set_point_size(get_interface_pause_size())
    text_entity = world.create_entity()
    c_surface = CSurface.from_text(
        get_interface_pause_text(),
        font,
        pygame.Color(get_interface_pause_color())
    )
    text_center = c_surface.surface.get_rect()
    text_center.center = screen.get_rect().center
    c_transform = CTransform(pygame.Vector2(text_center.x, text_center.y))

    world.add_component(text_entity, c_surface)
    world.add_component(text_entity, c_transform)
    world.add_component(text_entity, CTagPauseText())
    world.add_component(text_entity, CTagIsHidden())
    
def create_instructions_text(world: esper.World, screen: pygame.Surface):
    font: pygame.font.Font = ServiceLocator.texts_service.get_font(
        get_interface_font())
    font.set_point_size(get_interface_instructions_size())
    text_entity = world.create_entity()
    c_surface = CSurface.from_text(
        get_interface_instructions_text(),
        font,
        pygame.Color(get_interface_instructions_color())
    )
    
    text_pos = c_surface.surface.get_rect()
    text_pos.bottomleft = screen.get_rect().bottomleft
    c_transform = CTransform(pygame.Vector2(text_pos.x, text_pos.y))

    world.add_component(text_entity, c_surface)
    world.add_component(text_entity, c_transform)
    
def create_special_power_indicator(world: esper.World, screen: pygame.Surface, load: int):
    load_label = world.get_components(CTagLoadText)
    for entity, _ in load_label:
        world.delete_entity(entity)
    
    font: pygame.font.Font = ServiceLocator.texts_service.get_font(
        get_interface_font())
    font.set_point_size(get_interface_load_size())
    text_entity = world.create_entity()
    c_surface = CSurface.from_text(
        "Mines: " + str(load) + "%",
        font,
        pygame.Color(get_interface_load_color())
    )
    
    text_pos = c_surface.surface.get_rect()
    text_pos.bottomright = screen.get_rect().bottomright
    c_transform = CTransform(pygame.Vector2(text_pos.x, text_pos.y))

    world.add_component(text_entity, c_surface)
    world.add_component(text_entity, c_transform)
    world.add_component(text_entity, CTagLoadText())
    
def create_player_lifes_indicator(world: esper.World, screen: pygame.Surface, lifes: int):
    life_label = world.get_components(CTagLifesLabel)
    for entity, _ in life_label:
        world.delete_entity(entity)
    
    font: pygame.font.Font = ServiceLocator.texts_service.get_font(
        get_interface_font())
    font.set_point_size(get_interface_player_lifes_size())
    text_entity = world.create_entity()
    c_surface = CSurface.from_text(
        "Lifes: " + str(lifes),
        font,
        pygame.Color(get_interface_player_lifes_color())
    )
    
    text_pos = c_surface.surface.get_rect()
    text_pos.topright = screen.get_rect().topright
    c_transform = CTransform(pygame.Vector2(text_pos.x, text_pos.y))

    world.add_component(text_entity, c_surface)
    world.add_component(text_entity, c_transform)
    world.add_component(text_entity, CTagLifesLabel())     
    
def _set_animation(c_anim: CAnimation, anim_id: int):
    if c_anim.curr_anim == anim_id:
        return
    c_anim.curr_anim = anim_id
    c_anim.current_animation_time = 0
    c_anim.current_frame = c_anim.current_frame = c_anim.animation_list[c_anim.curr_anim].start
    