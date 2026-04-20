import pygame

class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Color):
        self.surface = pygame.Surface(size)
        self.surface.fill(color)
        self.area = self.surface.get_rect()
        
    @classmethod
    def from_surface(cls, surface: pygame.Surface):
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        c_surf.surface = surface
        c_surf.area = surface.get_rect()
        return c_surf
    
    
    @classmethod
    def from_text(cls, text: str, font: pygame.font.Font, color: pygame.Color):
        render_surf = font.render(text, True, color)
        return cls.from_surface(render_surf)
    
    @staticmethod
    def get_area_relative(area: pygame.Rect, pos_topleft: pygame.Vector2):
        relative_area = area.copy()
        relative_area.topleft = pos_topleft.copy()
        return relative_area