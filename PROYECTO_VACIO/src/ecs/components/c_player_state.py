from enum import Enum

from src.utils.config_loader import get_player_lifes

class CPlayerState:
    def __init__(self):
        self.state = PlayerState.IDLE
        self.lifes = get_player_lifes()
        
        
class PlayerState(Enum):
    IDLE = 0
    MOVE = 1