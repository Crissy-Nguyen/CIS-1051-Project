import pygame

pygame.init()

# Game window setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hopper')

# Player setup
player = pygame.Rect((400, 300, 50, 50))

run = True
while run:

    screen.fill((0, 0, 0))

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
