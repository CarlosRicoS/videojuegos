import esper
import pygame

from src.create.prefab_creator import create_special_power_indicator
from src.ecs.components.c_event_time import CEventTime
from src.ecs.components.tags.c_tag_expired_mines import CTagExpiredMines
from src.ecs.components.tags.c_tag_mine import CTagMine
from src.ecs.components.tags.c_tag_special_power_event import CTagSpecialPowerEvent
from src.utils.config_loader import get_special_bullet_reload_time


def system_special_load(world: esper.World, event_time: float, screen: pygame.Surface) -> None:
    especial_event = world.get_components(CEventTime, CTagSpecialPowerEvent)
    
    for entity, (c_event, _) in especial_event:
        
        loading_percentage = int((event_time - c_event.event_time) / get_special_bullet_reload_time() * 100)
        
        if loading_percentage >= 100:
            loading_percentage = 100
            world.delete_entity(entity)
            
            _clean_mines(world)
            
        create_special_power_indicator(world, screen, loading_percentage)
        
def _clean_mines(world: esper.World):
    mine_components = world.get_components(CTagMine)
    
    for mine_entity, _ in mine_components:
        world.remove_component(mine_entity, CTagMine)
        world.add_component(mine_entity, CTagExpiredMines())        
            
