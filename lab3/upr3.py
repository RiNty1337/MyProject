import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
RED = (255, 15, 15)

# Background
rect(screen, GRAY, (0, 0, 400, 400))
# Body
circle(screen, YELLOW, (200, 200), 100)
circle(screen, BLACK, (200, 200), 100, 1)
# Big eye
circle(screen, RED, (150, 180), 22)
circle(screen, BLACK, (150, 180), 22, 1)
circle(screen, BLACK, (150, 180), 9)
# Small eye
circle(screen, RED, (250, 180), 18)
circle(screen, BLACK, (250, 180), 18, 1)
circle(screen, BLACK, (250, 180), 7)
# Mouth
rect(screen, BLACK, (150, 250, 100, 20))
# Eyebrow left
pygame.draw.polygon(screen, BLACK, 
                    [[180, 175], [185, 165], 
                     [100, 100], [95, 110]])
# Eyebrow right
pygame.draw.polygon(screen, BLACK, 
                    [[225, 175], [220, 165], 
                     [290, 120], [295, 130]])



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()

