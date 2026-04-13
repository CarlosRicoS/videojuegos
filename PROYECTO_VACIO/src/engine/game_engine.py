import esper
import pygame

from src.create.prefab_creator import create_enemy_spawner, create_input_player, create_player_square, create_window, fill_window
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_bullet_lost import system_bullet_lost
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_explosion_remove import system_explosion_remove
from src.ecs.systems.s_hunter_follow_player import system_hunter_follow_player
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_player_limit_screen import system_player_limit_screen
from src.ecs.systems.s_player_shoot import system_player_shoot
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.utils.config_loader import get_framerate, get_level_01_events, get_player_spawn_position_config, get_player_velocity

class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.screen = create_window()
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = get_framerate()
        self.delta_time = 0
        self.elapsed_time = 0
        self.ecs_world = esper.World()
        

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(self.ecs_world, get_player_spawn_position_config())
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self.enemy_spawner = create_enemy_spawner(
            self.ecs_world, 
            spawn_events=get_level_01_events()
        )
        create_input_player(self.ecs_world)
        
    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        self.elapsed_time += self.delta_time

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.elapsed_time)
        system_movement(self.ecs_world, self.delta_time)
        system_hunter_follow_player(self.ecs_world, self._player_entity)
        system_player_state(self.ecs_world)
        system_hunter_state(self.ecs_world)
        system_screen_bounce(self.ecs_world, self.screen)
        system_bullet_lost(self.ecs_world, self.screen)
        system_player_limit_screen(self.ecs_world, self.screen, self._player_entity)
        system_collision_bullet_enemy(self.ecs_world, self._player_entity)
        system_collision_player_enemy(self.ecs_world, self._player_entity)
        system_explosion_remove(self.ecs_world)
        system_animation(self.ecs_world, self.delta_time)
        self.ecs_world._clear_dead_entities()
    
    def _draw(self):
        fill_window(self.screen)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        if c_input.name == 'PLAYER_LEFT':
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x -= get_player_velocity()
            elif c_input.phase == CommandPhase.END:    
                self._player_c_v.vel.x += get_player_velocity()
        elif c_input.name == 'PLAYER_RIGHT':
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x += get_player_velocity()
            elif c_input.phase == CommandPhase.END:    
                self._player_c_v.vel.x -= get_player_velocity()
        elif c_input.name == 'PLAYER_UP':
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.y -= get_player_velocity()
            elif c_input.phase == CommandPhase.END:    
                self._player_c_v.vel.y += get_player_velocity()
        elif c_input.name == 'PLAYER_DOWN':
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.y += get_player_velocity()
            elif c_input.phase == CommandPhase.END:    
                self._player_c_v.vel.y -= get_player_velocity()      
        elif c_input.name == 'PLAYER_FIRE':
            if c_input.phase == CommandPhase.START:
                system_player_shoot(
                    self.ecs_world, 
                    c_input.trigger_position, 
                    self._player_entity)
