import platforme as pl
import pygame
import player as p
import objects as obp

class Level:
    def __init__(self, a) -> None:
        self.platforms = []
        self.objects = []
    
    n = 0

    def loadLevel(self, level):
        if level == 1:
            pla = [pl.Platform(10, 420, 400, 40, (100, 200, 0))]
            self.platforms = pla
        if level == 2:
            pla = [pl.Platform(10, 420, 400, 40, (230, 0, 0))]
            self.platforms = pla
        if level == 3:
            pla = [pl.Platform(10, 100, 140, 40, (230, 0, 0))
                   , pl.Platform(80, 400, 200, 40, (93, 0, 230))
                   , pl.Platform(220, 300, 200, 40, (47, 0, 230))
                   , pl.Platform(220, 180, 40, 20, (239, 0, 230))]
            self.platforms = pla

    def number(self):
        return self.n
    
    def updateLevel(self):
        pass

    def renderLevel(self, screen):
        for platform in self.getLevelPlatforms():
            platform.render(screen=screen)
        for objectt in self.getLevelObjects():
            objectt.render(screen=screen)
    
    def getLevelPlatforms(self):
        return self.platforms

    def getLevelObjects(self):
        return self.objects
    
    def loadFromFile(self, text):
        platforms = []
        objects = []
        sp = [0, 0]
        with open("./levels/" + text, 'rt') as level:
            data = level.read().strip()  # Read the file content and remove leading/trailing whitespaces
            entries = data.split(';')   # Split the data into individual platform entries
            
            for entry in entries:
                elements = entry.split(',')  # Split each entry into individual elements
                # Spawn point
                if len(elements) == 4 and elements[3] == "sp":
                    sp[0] = elements[0]
                    sp[1] = elements[1]
                    #pId = elements[2]
                
                if len(elements) == 8 and elements[7] == "p":  # Ensure each entry has 7 elements (4 for position, 3 for color, 1 for ensuring it is a platform (id 0)
                    platform = pl.Platform(int(elements[0]),
                                           int(elements[1]),
                                           int(elements[2]),
                                           int(elements[3]),
                                           (int(elements[4]), int(elements[5]), int(elements[6]))
                                           )
                    platforms.append(platform)
                
                # x,y,w,h,powerId,o
                if len(elements) == 6 and elements[5] == "o": # Ensure it is an object
                    x = int(elements[0])
                    y = int(elements[1])
                    w = int(elements[2])
                    h = int(elements[3])
                    power = int(elements[4])
                    
                    
                    obj = obp.Object(x, y, w, h, power)
                    if power == 1:
                        obj.setColor((2, 170, 100))
                    
                    objects.append(obj)

        self.platforms = platforms
        self.objects = objects
        return (platforms, objects, sp)