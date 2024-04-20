import pygame


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surface = pygame.Surface(size)
        self.surface.fill(color)
        self.area = self.surface.get_rect()

    @classmethod
    def from_surface(cls, surface: pygame.Surface) -> "CSurface":
        instance = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        instance.surface = surface
        instance.area = instance.surface.get_rect()
        return instance
