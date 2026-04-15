from enum import Enum

import pygame


class CHunterState:
    def __init__(self, origin: pygame.Vector2):
        self.origin = origin
        self.state = HunterState.IDLE
        self.is_returning = False
        
class HunterState(Enum):
    IDLE = 0
    MOVE = 1