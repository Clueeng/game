import pygame
import platforme as pl
import levels
from random import randint

class Player:

    x = 0
    y = 0
    width, height = 32, 64
    velX = 0
    velY = 0
    friction = 0.90
    gravity = 1
    motionY = -15
    color = (220, 20, 100)
    airborn = False

    # controls
    left = pygame.K_a
    right = pygame.K_d
    spX: int = 10
    spY: int = 10

    screen_height = 0
    screen_width = 0

    def setSpawnPoint(self, x: int, y: int):
        self.spX = x
        self.spY = y

    def setScreenDimensions(self, dimension):
        self.screen_height = dimension[1]
        self.screen_width = dimension[0]

    currentLevel = None

    def setLevel(self, level):
        self.currentLevel = level

    hitbox = pygame.Rect(x, y, width, height)

    def __init__(self) -> None:
        self.spawn()

    def spawn(self):
        #self.airborn = True
        #self.jump = False
        self.x = self.spX
        self.y = self.spY
        self.velX = 0
        self.velY = 0
    
    def jump(self):
        if not self.airborn:
            self.velY = self.motionY
            #self.velX = 3 * self.getDirection()
        self.airborn = True
    
    def debugCheats(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_e]:
            self.gravity = 0 # def: 1
            self.velY = -10
            self.jump()

        if pressed[pygame.K_g]:
            self.motionY = -40
    
    def move(self, speed):

        pressed = pygame.key.get_pressed()
        direction = self.getDirection()
        if direction == -1:
            self.velX -= speed
        elif direction == 1:
            self.velX += speed

        self.x += self.velX

        if pressed[pygame.K_SPACE]:
            self.jump()
        
        self.gravity = 1
        self.motionY = -15
        self.debugCheats()

        # Gravity logic
        if self.velY < 30:
            self.velY += self.gravity
        self.y += self.velY

        #print(self.velY)

        

    def objectCollision(self):
        for objectt in self.currentLevel.getLevelObjects():
            player = self.hitbox
            obj = objectt.hitbox
            powerId = objectt.powerId
            colliding = player.colliderect(obj)
            if colliding:
                #print("A " + str(randint(1, 4)))
                if powerId == 1: # Jump pad
                    self.velY = - 20
                if powerId == 2: # Spawn Point
                    print("end of level idk") 
                if powerId == 3:
                    print("death")
                    self.spawn()
                self.currentLevel.objects.remove(objectt)

    
    def collisionChecks(self):
        for platform in self.currentLevel.getLevelPlatforms():
            playerBottom = self.y + self.height
            playerTop = self.y
            playerLeft = self.x
            playerRight = self.x + self.width
            platLeft = platform.hitbox.left
            platRight = platform.hitbox.right
            platformBottom = platform.hitbox.bottom
            platformTop = platform.hitbox.top

            betweenPlat = playerRight >= platLeft and playerLeft <= platRight
            
            touchingRight = playerLeft >= platRight - min(16, platform.hitbox.w) and playerLeft <= platRight
            touchingLeft = playerRight <= platLeft + min(16, platform.hitbox.w) and playerRight >= platLeft
            underPlatform = playerTop <= platformBottom and playerTop >= platformTop
            abovePlatform = playerBottom >= platformTop and playerBottom <= platformTop + 20
            onSameLevel = (playerBottom >= platformTop and playerTop <= platformBottom) or (playerTop <= platformBottom and playerBottom >= platformTop)
            #isBetweenVertically = (playerTop <= platformTop and playerBottom >= platformBottom)
            
            #if underPlatform and betweenPlat:
                #self.velY = 0
                #self.airborn = True
                #self.y = platformTop - self.height
                #print("hit your head dummy")
            if underPlatform and betweenPlat:
                self.velX = 0
                if touchingLeft:
                    print("Touching left")
                    #self.x = platLeft - self.width
                    #self.hitbox.colliderect(self.hitbox.x * self.velX, self.hitbox.y * self.velY, self.hitbox.w, self.hitbox.h)
                if touchingRight:
                    print("Touching right")
                    #self.hitbox.colliderect(self.hitbox.x * self.velX, self.hitbox.y * self.velY, self.hitbox.w, self.hitbox.h)
                    #self.x = platRight

            if abovePlatform and betweenPlat:
                self.velY = 0
                self.airborn = False
                self.y = platformTop - self.height

            if playerTop >= self.screen_height:
                newLevel = self.currentLevel
                newLevel.loadLevel(self.currentLevel.number())
                print("fell off the level pookie")
                self.spawn()

    
    def getDirection(self):
        pressed = pygame.key.get_pressed()
        if pressed[self.left]: return -1
        if pressed[self.right]: return 1
        if not pressed[self.left] and not pressed[self.right]: return 0
    
    def update(self):
        self.velX *= self.friction
        self.velY *= self.gravity
        self.collisionChecks()
        self.objectCollision()
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.hitbox)