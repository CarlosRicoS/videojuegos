import pygame

class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Color):
        self.surface = pygame.Surface(size)
        self.surface.fill(color)