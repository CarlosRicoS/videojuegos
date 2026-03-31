import esper
import pygame

from src.create.prefab_creator import create_enemy_spawner, create_window, fill_window
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.utils.config_loader import get_enemy_color, get_enemy_list, get_enemy_size, get_enemy_velocity_range, get_framerate, get_level_01_events

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
        self.enemy_spawner = create_enemy_spawner(
            self.ecs_world, 
            spawn_events=get_level_01_events()
        )
        
    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        self.elapsed_time += self.delta_time

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.elapsed_time)
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
    
    def _draw(self):
        fill_window(self.screen)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()
