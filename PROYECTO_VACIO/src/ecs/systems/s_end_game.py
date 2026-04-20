import esper
import pygame

from src.create.prefab_creator import create_end_game_message
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_game_state import CGameState, GameStateEnum
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_hunter import CTagHunter

def system_end_game(world: esper.World, screen: pygame.Surface, player_entity: int):
    components = world.get_component(CGameState)
    
    spawner = world.get_component(CEnemySpawner)
    pending_spawn_events = 0
    is_winner: bool
    player_lifes = world.component_for_entity(player_entity, CPlayerState).lifes    
    for _, (c_es) in spawner:
        pending_spawn_events = len([ev for ev in c_es.spawn_events if all(ev.values())])
    
    c_gs: CGameState
    
    for _, (c_gs) in components:
        enemies_count = len(world.get_components(CTagEnemy))
        hunters_count = len(world.get_components(CTagHunter))   
        
        if(enemies_count == 0 and hunters_count == 0 and pending_spawn_events == len(c_es.spawn_events)):
            is_winner = True
            c_gs.state = GameStateEnum.GAME_OVER
            
        if player_lifes <= 0:
            is_winner = False
            c_gs.state = GameStateEnum.GAME_OVER
            
        if c_gs.state == GameStateEnum.GAME_OVER:
            create_end_game_message(world, screen, is_winner)