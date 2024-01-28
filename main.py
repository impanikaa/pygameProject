import pygame

pygame.init()
width, height = 900, 600
screen = pygame.display.set_mode((width, height))

background_image = pygame.image.load("data/background.png")

shop_button_rect = pygame.Rect(30, 20, 200, 65)
shop_button_color = (255, 194, 38)
shop_button_corner_radius = 10

help_button_rect = pygame.Rect(730, 20, 65, 65)
help_button_color = (255, 194, 38)
help_button_corner_radius = 10
help_button_icon = pygame.image.load("data/help.png")  # Замените "data/help.png" на путь к изображению размером 30x30

setting_button_rect = pygame.Rect(810, 20, 65, 65)
setting_button_color = (255, 194, 38)
setting_button_corner_radius = 10
setting_button_icon = pygame.image.load("data/setting.png")  # Замените "data/setting.png" на путь к изображению размером 30x30

text_color = (0, 2, 18)
font = pygame.font.SysFont(None, 32)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))

    pygame.draw.rect(screen, shop_button_color, shop_button_rect, border_radius=shop_button_corner_radius)
    text1 = font.render("Магазин", True, text_color)
    text1_rect = text1.get_rect(center=shop_button_rect.center)
    screen.blit(text1, text1_rect)

    pygame.draw.rect(screen, help_button_color, help_button_rect, border_radius=help_button_corner_radius)
    screen.blit(help_button_icon, (help_button_rect.centerx - help_button_icon.get_width() // 2, help_button_rect.centery - help_button_icon.get_height() // 2))

    pygame.draw.rect(screen, setting_button_color, setting_button_rect, border_radius=setting_button_corner_radius)
    screen.blit(setting_button_icon, (setting_button_rect.centerx - setting_button_icon.get_width() // 2, setting_button_rect.centery - setting_button_icon.get_height() // 2))

    pygame.display.flip()

pygame.quit()
