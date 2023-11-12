import pygame

pygame.init()

# Game window setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hopper')

# Define game variables
tile_size = 50

def draw_grid():
    for line in range(12):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
    for line in range(16):
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))

# Character setup
class char(pygame.sprite.Sprite):
    def create(self, x, y):
        pygame.sprite.Sprite.create(self)
        
player = pygame.Rect((400, 300, 50, 50))

run = True
while run:

    screen.fill((0, 0, 0))
    draw_grid()

    pygame.draw.rect(screen, (255, 255, 0), player)

    # Player controls
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0)
    if key[pygame.K_d] == True:
        player.move_ip(1, 0)
    if key[pygame.K_w] == True:
        player.move_ip(0, -1)
    if key[pygame.K_s] == True:
        player.move_ip(0, 1)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()
