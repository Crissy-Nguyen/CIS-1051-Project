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
        self.image = pygame.transform.scale(img, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
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
        for t in world.tiles:
            # In x direction
            if t[1].colliderect(self.rect.x + change_x, self.rect.y, self.width, self.height):
                change_x = 0
            # In y direction
            if t[1].colliderect(self.rect.x, self.rect.y + change_y, self.width, self.height):
                # Check if player is below the ground (i.e. jumping)
                if self.vel_y < 0:
                    change_y = t[1].bottom - self.rect.top
                    self.vel_y = 0
                # Check if player is above the ground (i.e. falling)
                elif self.vel_y >= 0:
                    change_y = t[1].top - self.rect.bottom
                    self.vel_y = 0

        # Update player coords
        self.rect.x += change_x
        self.rect.y += change_y

        # Temporary floor
        '''if self.rect.bottom > screen_height-48:
            self.rect.bottom = screen_height-48
            change_y = 0
        '''
        
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
                    tile = (img, img_rect)
                    self.tiles.append(tile)
                if tile == -1:
                    img = pygame.transform.scale(carrot, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tiles.append(tile)
                col_count += 1
                if tile == 2:
                    spike = Spike(col_count * tile_size - 39.5, row_count * tile_size + 16)
                    spike_group.add(spike)
            row_count += 1

    def draw(self):
        for t in self.tiles:
            screen.blit(t[0], t[1])
            pygame.draw.rect(screen, (255, 0, 255), t[1], 2)
            
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('sprites/things/2.png')
        self.image = pygame.transform.scale(self.img, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

world_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0], 
[0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], 
[1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1]
]

player = Player(48*2, 48*8)

spike_group = pygame.sprite.Group()

world = World(world_data)

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    world.draw()
    spike_group.draw(screen)
    player.update()
    player.flippy()
    #draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
