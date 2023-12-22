import pygame
import player as pl
import screen as sc
import levels
import objects as objs
import random
import platforme as pla
import string

pygame.init()

running = True
clock = pygame.time.Clock()
window = sc.screen(820, 620)
screen = window.getScreen()
holding = False
oldPos = (0, 0)
stopped = False

platforms = []
objects = []
saveFile = ""
directory = "./levels/"

mode = 0

def getModeName():
    if mode == 0:
        return "Builder"
    if mode == 1:
        return "Eraser"
    if mode == 2:
        return "Spawn Point"
    return "Null"

def draw_text(text, font_size, x, y, color):
    font = pygame.font.Font(None, font_size)  # You can specify a font file or use None for default font and size
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def get_text_size(text, font_size):
    font = pygame.font.Font(None, font_size)  # You can specify a font file or use None for default font and size
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface.get_size()

rectToSave = None
name = ''.join(random.choice(string.ascii_lowercase) for i in range(12))
saved = ""
while running:
    pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            holding = True
            oldPos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            if holding:
                stopped = True
            holding = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                print("Saving file")
                saved = f"Saved {name}"
                
                #lvl = f"{x},{y},{w},{h},255,0,0,p;"
                for p in platforms:
                    p: pla.Platform
                    x, y, w, h = p.hitbox.x, p.hitbox.y, p.hitbox.width, p.hitbox.height
                    r, g, b = p.color  # Extract color components
                    save_data = f"{x},{y},{w},{h},{r},{g},{b},p;"
                    saveFile += save_data
                for o in objects:
                    o: objs.Object
                    x, y = o.hitbox.x, o.hitbox.y
                    pId = o.powerId
                    save_data = f"{x},{y},{pId},sp;"
                    saveFile += save_data
                with open(f"{directory}{name}.txt", 'w') as f:
                    f.write(saveFile)
            if event.key == pygame.K_1:
                mode = 0
            if event.key == pygame.K_2:
                mode = 1
            if event.key == pygame.K_3:
                mode = 2
    
    # Refresh from last frame
    screen.fill(window.getColor())

    if holding:
        mp = pygame.mouse.get_pos()
        if mode == 0:
            sel = (
                min(oldPos[0], mp[0]), min(oldPos[1], mp[1]),
                abs(oldPos[0]-mp[0]), abs(oldPos[1] - mp[1])
            )
            rect = pygame.Rect(sel)
            pygame.draw.rect(screen, (255, 0, 0), rect)
            rectToSave = rect
        if mode == 1:
            mouse_pos = pygame.mouse.get_pos()
            for platform in platforms:
                if platform.hitbox.collidepoint(mouse_pos):
                    platforms.remove(platform)
            for objec in objects:
                if objec.hitbox.collidepoint(mouse_pos):
                    objects.remove(objec)
        if mode == 2:
            mouse_pos = pygame.mouse.get_pos()


    
    if stopped:
        if mode == 0:
            x = min(oldPos[0], mp[0])
            y = min(oldPos[1], mp[1])
            w = abs(oldPos[0]-mp[0])
            h = abs(oldPos[1] - mp[1])
            platforms.append(pla.Platform(x, y, w, h, (255, 0, 0)))
        if mode == 2:
            objects.append(objs.Object.spawnPoint(mouse_pos[0], mouse_pos[1]))

        stopped = False
    
    for platform in platforms:
        platform.render(screen=screen)
    for objec in objects:
        objec: objs.Object
        objec.render(screen=screen)

    
    draw_text("Editing a level", 32, 335, 10, (255, 255, 255))
    draw_text(saved, 32, (820/2) - (get_text_size(saved, 32)[0]/2), 30, (255, 255, 255))
    draw_text("Mode: " + getModeName(), 32, (820/2) - (get_text_size("Mode: " + getModeName(), 32)[0]/2), (620-20), (255, 255, 255))
    

    
    pygame.display.update()
    clock.tick(60)