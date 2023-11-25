import pygame

pygame.init()

# Game window setup
screen_width = 800
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hopper')

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# game variables
GRAVITY = 0.5

# Tile measurement
'''tile_size = 32
def draw_grid():
    for line in range(15):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
    for line in range(25):
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))
'''
# Player action variables
left = False
right = False
shoot = False

# Load images
carrot = pygame.image.load('sprites/things/0.png').convert_alpha()

def draw_bg():
    screen.fill((143, 191, 190))
    pygame.draw.line(screen, (255, 0, 0), (0, 400), (screen_width, 400))


# Character setup
class char(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.midair = True
        self.flip = False
        self.animations = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        for i in range (2):
            img = pygame.image.load(f'sprites/{self.char_type}/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animations.append(img)
        self.image = self.animations[self.index]
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, left, right):
        change_x = 0
        change_y = 0

        # Moving left and right
        if left:
            change_x = -self.speed
            self.flip = True
            self.direction = -1 
        if right:
            change_x = self.speed
            self.flip = False
            self.direction = 1

        # Jump 
        if self.jump == True and self.midair == False:
            self.vel_y = -10
            self.jump = False
            self.midair = True

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        change_y += self.vel_y

        # Check collision with floor
        if self.rect.bottom + change_y > 400:
            change_y = 400 - self.rect.bottom
            self.midair = False

        self.rect.x += change_x
        self.rect.y += change_y

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
        
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = carrot
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

proj_group = pygame.sprite.Group()




player = char('player', 200, 200, 3, 5)



# Game running
run = True
while run:

    clock.tick(FPS)

    draw_bg()
    #draw_grid()

    player.draw()
    player.move(left, right)

    proj_group.update()
    proj_group.draw(screen)

    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
                run = False

        # Player keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
    
        # Player keyboard release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
            
    pygame.display.update()
pygame.quit()
