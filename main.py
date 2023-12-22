import pygame
import player as pl
import screen as sc
import levels

pygame.init()

running = True
clock = pygame.time.Clock()
window = sc.screen(820, 620)
screen = window.getScreen()


level = levels.Level("a")
#level.loadFromFile('levels.txt')
l = level.loadFromFile("kgahnfajuhof.txt")
player = pl.Player()
player.setSpawnPoint(int(l[2][0]), int(l[2][1]))
player.spawn()
player.setLevel(level)
player.setScreenDimensions(window.getDimension())

# find a way to access current level from main to player

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Refresh from last frame
    screen.fill(window.getColor())
    
    level.updateLevel()
    level.renderLevel(screen)

    player.update()
    player.move(1)

    player.render(screen)
    pygame.display.update()
    clock.tick(60)