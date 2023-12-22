import pygame
class screen:
    width = 0
    height = 0
    r = 0
    g = 0
    b = 0

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

    def getDimension(self):
        return (self.width, self.height)
    
    def getScreen(self):
        return pygame.display.set_mode(self.getDimension())
    
    def setTitle(title):
        pygame.display.set_caption(title=title)
    
    def getColor(self):
        return (self.r, self.g, self.b)