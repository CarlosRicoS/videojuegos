import esper

from src.ecs.components.c_game_state import CGameState, GameStateEnum
from src.ecs.components.tags.c_tag_is_hidden import CTagIsHidden
from src.ecs.components.tags.c_tag_pause_text import CTagPauseText


def system_game_state(world: esper.World, input_command_name: str):
    components = world.get_component(CGameState)
    pause_text = world._get_component(CTagPauseText)
    
    c_gs: CGameState
    pause_text_entity: int
    
    for entity, _ in pause_text:
        pause_text_entity = entity
    
    for _, (c_gs) in components:
        if input_command_name != 'PLAYER_PAUSE':
            continue
        if c_gs.state == GameStateEnum.PLAYING:
            if world.has_component(pause_text_entity, CTagIsHidden):
                world.remove_component(pause_text_entity, CTagIsHidden)
            c_gs.state = GameStateEnum.PAUSED
        elif c_gs.state == GameStateEnum.PAUSED:
            world.add_component(pause_text_entity, CTagIsHidden())
            # for _, c_input in world.get_component(CInputCommand):
            #     c_input.phase = CommandPhase.END 
            c_gs.state = GameStateEnum.PLAYING
            