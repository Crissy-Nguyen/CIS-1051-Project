import random
import pygame
from pygame.locals import *

pygame.init()

# Game window setup
screen_width = 576
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('test')

clock = pygame.time.Clock()
FPS = 60

# Create a single color background
def draw_bg():
    screen.fill((143, 191, 190))

# Grid setup for measurement purposes
tile_size = 48
def draw_grid():
    for line in range(15):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
    for line in range(25):
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

# Player setup
class Player():
    def __init__(self, x, y):
        img = pygame.image.load('sprites/player/0.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.flip = False
        self.direction = 0

    def update(self):

        change_x = 0
        change_y = 0
        
        # Key presses
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.jumped == False:
            self.vel_y = -12
            self.jumped = True
        if key[pygame.K_w] == False:
            self.jumped = False
        if key[pygame.K_a]:
            change_x -= 5
            self.flip = True
        if key[pygame.K_d]:
            change_x += 5
            self.flip = False
        
        # Gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        change_y += self.vel_y

        # Check for collision

        # Update player coords
        self.rect.x += change_x
        self.rect.y += change_y

        # Temporary floor
        if self.rect.bottom > screen_height-48:
            self.rect.bottom = screen_height-48
            change_y = 0
            
        # Draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 0), self.rect, 2)

    def flippy(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# World setup
class World():
    def __init__(self, data):
        self.tiles = []

        # Some images
        block = pygame.image.load('sprites/things/1.png')
        carrot = pygame.image.load('sprites/things/0.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(block, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    t = (img, img_rect)
                    self.tiles.append(t)
                if tile == -1:
                    img = pygame.transform.scale(carrot, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    t = (img, img_rect)
                    self.tiles.append(t)
                col_count += 1
            row_count += 1

    def draw(self):
        for i in self.tiles:
            screen.blit(i[0], i[1])
            

world_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, random.randint(-1,0), 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(48*2, 48*8)

world = World(world_data)

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    world.draw()
    player.update()
    player.flippy()
    #draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
