from enum import Enum

class CGameState:
    def __init__(self):
        self.state = GameStateEnum.PLAYING
        
class GameStateEnum(Enum):
    PLAYING = 0
    PAUSED = 1
    GAME_OVER = 2