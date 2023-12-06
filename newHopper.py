import random
import pygame
from pygame.locals import *

pygame.init()

# Framerate setup
clock = pygame.time.Clock()
FPS = 60

# Game window setup
screen_width = 576
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hopper')

# Font setup
font0 = pygame.font.SysFont('Courier', 30)
font1 = pygame.font.SysFont('Courier', 60)
white = (255, 255, 255)
red = (255, 0, 0)


# Single color background setup
def draw_bg():
    screen.fill((143, 191, 190))

#Score counter setup
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

# Button class for buttons that appear upon Game Over
retry_img = pygame.image.load('sprites/buttons/0.png')
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        
    def draw(self):
        action = False
        
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Conditions for when a button is pressed
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        # Draw button
        screen.blit(self.image, self.rect)

        return action

game_over = False
score = 0

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
        # Scroll down to the reset function
        self.reset(x, y)

    def update(self, game_over):

        change_x = 0
        change_y = 0

        # Player stops moving when dead
        if game_over == False:
        
            # Key presses
            key = pygame.key.get_pressed()
            # Jumping
            if key[pygame.K_UP] and self.jumped == False and self.helpless == False:
                self.vel_y = -11
                self.jumped = True
            if key[pygame.K_UP] == False:
                self.jumped = False
            # Moving left or right
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

            # Collision check
            #self.helpless = True
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
                        self.helpless = False
                        

            # Check for collision with hazards
            if pygame.sprite.spritecollide(self, spike_group, False):
                game_over = True
                print("You died.")
            
            # Update player coords
            self.rect.x += change_x
            self.rect.y += change_y

        # Player sprite changes when hitting a hazard
        elif game_over:
            self.image = self.dead_image

        # Temporary floor
        '''if self.rect.bottom > screen_height-48:
            self.rect.bottom = screen_height-48
            change_y = 0
        '''
        
        # Draw player onto screen
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 0), self.rect, 2)

        return game_over

    # Player stuff; reset player every time user clicks the Retry button
    def reset(self, x, y):
        img = pygame.image.load('sprites/player/0.png')
        self.image = pygame.transform.scale(img, (32, 32))
        dead_img = pygame.image.load('sprites/player/1.png')
        self.dead_image = pygame.transform.scale(dead_img, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.flip = False
        self.direction = 0
        self.helpless = True

    # Sprite will visibly switch directions
    def flippy(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# World setup
class World():
    def __init__(self, data):
        self.reset(data)

    def draw(self):
        for t in self.tiles:
            screen.blit(t[0], t[1])
            #pygame.draw.rect(screen, (255, 0, 255), t[1], 2)

    def reset(self, data):
        self.tiles = []
        hasCarrot = False

        # Some images
        block = pygame.image.load('sprites/things/1.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                # 1: Block
                if tile == 1:
                    img = pygame.transform.scale(block, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tiles.append(tile)
                # -1: Carrot
                if tile == -1:
                    hasCarrot = True
                    carrot = Carrot(col_count*tile_size, row_count*tile_size)
                    carrot_group.add(carrot)
                # 2: Spike
                if tile == 2:
                    spike = Spike(col_count*tile_size + 8, row_count*tile_size + 8)
                    spike_group.add(spike)
                col_count += 1
            row_count += 1

# Hazard setup            
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('sprites/things/2.png')
        self.image = pygame.transform.scale(self.img, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Carrot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('sprites/things/0.png')
        self.image = pygame.transform.scale(self.img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


player = Player(48*2, 48*8)

spike_group = pygame.sprite.Group()
carrot_group = pygame.sprite.Group()

world = World([
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, random.randint(-1,0), 0, 0, 0, 0, 0, 0, 0, 0, random.randint(-1,0), 0],
[0, random.choice([0,2]), 0, 0, 0, 0, 0, 0, 0, 0, random.choice([0,2]), 0],
[0, 1, 1, 0, random.randint(1,2), random.randint(1,2), random.randint(1,2), random.randint(1,2), 0, 1, 1, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, random.randint(1,2), 0, 0, 0, 1, 1, 0, 0, 0, random.randint(1,2), 0], 
[0, random.choice([0,2]), 0, 0, 0, random.choice([0,2]), random.choice([0,2]), 0, 0, 0, random.choice([0,2]), 0], 
[random.randint(0,2), 1, 0, 0, random.randint(1,2), 1, 1, random.randint(1,2), 0, 0, 1, random.randint(0,2)], 
[0, random.randint(-1,0), 0, 0, 0, random.choice([0,2]), random.choice([0,2]), 0, 0, 0, random.randint(-1,0), 0], 
[1, 1, 1, 1, random.randint(0,2), random.randint(0,2), random.randint(0,2), random.randint(0,2), 1, 1, 1, 1]
])

retry = Button(48*2, 48*6, retry_img)

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    
    world.draw()

    if game_over == False:
        if pygame.sprite.spritecollide(player, carrot_group, True):
            score += 1
            print(score)
            spike_group = pygame.sprite.Group()
            carrot_group = pygame.sprite.Group()
            world.reset([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, random.randint(-1,0), 0, 0, 0, 0, 0, 0, 0, 0, random.randint(-1,0), 0],
            [0, random.choice([0,2]), 0, 0, 0, 0, 0, 0, 0, 0, random.choice([0,2]), 0],
            [0, 1, 1, 0, random.randint(1,2), random.randint(1,2), random.randint(1,2), random.randint(1,2), 0, 1, 1, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, random.randint(1,2), 0, 0, 0, 1, 1, 0, 0, 0, random.randint(1,2), 0], 
            [0, random.choice([0,2]), 0, 0, 0, random.choice([0,2]), random.choice([0,2]), 0, 0, 0, random.choice([0,2]), 0], 
            [random.randint(0,2), 1, 0, 0, random.randint(1,2), 1, 1, random.randint(1,2), 0, 0, 1, random.randint(0,2)], 
            [0, random.randint(-1,0), 0, 0, 0, random.choice([0,2]), random.choice([0,2]), 0, 0, 0, random.randint(-1,0), 0], 
            [1, 1, 1, 1, random.randint(0,2), random.randint(0,2), random.randint(0,2), random.randint(0,2), 1, 1, 1, 1]
            ])
        draw_text("Score: " + str(score), font0, white, 48*1, 0)
    
    spike_group.draw(screen)
    carrot_group.draw(screen)
    
    game_over = player.update(game_over)

    if game_over:
        draw_text("GAME OVER", font1, red, 48*2.5, 48*2)
        if retry.draw():
            player.reset(48*2, 48*8)
            spike_group = pygame.sprite.Group()
            carrot_group = pygame.sprite.Group()
            world.reset([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, random.randint(-1,0), 0, 0, 0, 0, 0, 0, 0, 0, random.randint(-1,0), 0],
            [0, random.choice([0,2]), 0, 0, 0, 0, 0, 0, 0, 0, random.choice([0,2]), 0],
            [0, 1, 1, 0, random.randint(1,2), random.randint(1,2), random.randint(1,2), random.randint(1,2), 0, 1, 1, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, random.randint(1,2), 0, 0, 0, 1, 1, 0, 0, 0, random.randint(1,2), 0], 
            [0, random.choice([0,2]), 0, 0, 0, random.choice([0,2]), random.choice([0,2]), 0, 0, 0, random.choice([0,2]), 0], 
            [random.randint(0,2), 1, 0, 0, random.randint(1,2), 1, 1, random.randint(1,2), 0, 0, 1, random.randint(0,2)], 
            [0, random.randint(-1,0), 0, 0, 0, random.choice([0,2]), random.choice([0,2]), 0, 0, 0, random.randint(-1,0), 0], 
            [1, 1, 1, 1, random.randint(0,2), random.randint(0,2), random.randint(0,2), random.randint(0,2), 1, 1, 1, 1]
            ])
            score = 0
            game_over = False
    
    player.flippy()
    
    #draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
