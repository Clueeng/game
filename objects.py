import pygame

class Object:

    hitbox: pygame.Rect = None

    def __init__(self, x, y, w, h, powerId):
        self.hitbox = pygame.Rect(x, y, w, h)
        self.powerId = powerId
    
    color = (255, 255, 255)

    def setColor(self, col: tuple):
        self.color = col
        return self.color
    
    def render(self, screen: pygame.Surface):
        if self.powerId == 2: # Spawn point
            self.setColor((10, 230, 20))
        if self.powerId == 1: # Pad
            self.color((90, 35, 230))
        pygame.draw.rect(screen, self.color, self.hitbox)
    
    def spawnPoint(x, y):
        return Object(x, y, 16, 16, 2)