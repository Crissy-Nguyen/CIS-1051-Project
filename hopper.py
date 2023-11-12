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

# Tile measurement
tile_size = 32
def draw_grid():
    for line in range(15):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
    for line in range(25):
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

# Player action variables
left = False
right = False

def draw_bg():
    screen.fill((0, 0, 0))

# Character setup
class char(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        img = pygame.image.load(f'sprites/{self.char_type}/Sprite-0001.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, left, right):
        change_x = 0
        change_y = 0
        if left:
            change_x = -self.speed
            self.flip = True
            self.direction = -1
        if right:
            change_x = self.speed
            self.flip = False
            self.direction = 1
        self.rect.x += change_x
        self.rect.y += change_y

        
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
player = char('player', 200, 200, 3, 5)



# Game running
run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()

    player.draw()
    player.move(left, right)


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
    
        # Player keyboard release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
            
    pygame.display.update()
pygame.quit()
