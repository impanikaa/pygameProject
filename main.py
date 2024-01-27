import pygame


pygame.init()
width, height = 900, 600
screen = pygame.display.set_mode((width, height))

background_image = pygame.image.load("data/background.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background_image, (0, 0))

    pygame.display.flip()

pygame.quit()