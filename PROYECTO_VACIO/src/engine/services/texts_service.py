import pygame


class TextsService:
    def __init__(self):
        self._fonts = {}

    def get_font(self, path: str):
        if path not in self._fonts:
            self._fonts[path] = pygame.font.Font(path)
        return self._fonts[path]