import pygame

class CTransform:
    def __init__(self, pos: pygame.Vector2):
        self.pos = pos
        
    @classmethod
    def from_original_position(cls, pos: pygame.Vector2):
        c_trans = cls(pos)
        c_trans.origin = pos.copy()
        return c_trans        