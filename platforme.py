import pygame

class Platform:
    def __init__(self, x, y, width, height, color: tuple):
        self.hitbox = pygame.Rect(x, y, width, height)
        self.color = color
    
    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.hitbox)