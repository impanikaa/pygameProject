import pygame
import math

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
help_button_icon = pygame.image.load("data/help.png")

setting_button_rect = pygame.Rect(810, 20, 65, 65)
setting_button_color = (255, 194, 38)
setting_button_corner_radius = 10
setting_button_icon = pygame.image.load("data/setting.png")

planet1_image = pygame.image.load("data/planet1.png")
planet2_image = pygame.image.load("data/planet2.png")
planet3_image = pygame.image.load("data/planet3.png")
planet4_image = pygame.image.load("data/planet4.png")

# Орбиты
orbit_1 = pygame.Rect(280, 75, 450, 450)
orbit_2 = pygame.Rect(340, 135, 330, 330)
orbit_3 = pygame.Rect(390, 185, 230, 230)
orbit_4 = pygame.Rect(440, 235, 130, 130)

# Угловые скорости для каждой планеты (в радианах в секунду)
angular_speed_1 = 0.00007
angular_speed_2 = 0.0002
angular_speed_3 = 0.00035
angular_speed_4 = 0.0005

text_color = (0, 2, 18)
font = pygame.font.SysFont(None, 32)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background_image, (0, 0))

    # Обновление углов планет
    angle_1 = pygame.time.get_ticks() * angular_speed_1
    angle_2 = pygame.time.get_ticks() * angular_speed_2
    angle_3 = pygame.time.get_ticks() * angular_speed_3
    angle_4 = pygame.time.get_ticks() * angular_speed_4

    # Рассчитываем координаты планет вдоль орбит
    planet1_x = int(orbit_1.centerx + orbit_1.width / 2 * math.cos(angle_1))
    planet1_y = int(orbit_1.centery + orbit_1.height / 2 * math.sin(angle_1))

    planet2_x = int(orbit_2.centerx + orbit_2.width / 2 * math.cos(angle_2))
    planet2_y = int(orbit_2.centery + orbit_2.height / 2 * math.sin(angle_2))

    planet3_x = int(orbit_3.centerx + orbit_3.width / 2 * math.cos(angle_3))
    planet3_y = int(orbit_3.centery + orbit_3.height / 2 * math.sin(angle_3))

    planet4_x = int(orbit_4.centerx + orbit_4.width / 2 * math.cos(angle_4))
    planet4_y = int(orbit_4.centery + orbit_4.height / 2 * math.sin(angle_4))

    # Отрисовка планет
    screen.blit(planet1_image, (planet1_x - planet1_image.get_width() // 2, planet1_y - planet1_image.get_height() // 2))
    screen.blit(planet2_image, (planet2_x - planet2_image.get_width() // 2, planet2_y - planet2_image.get_height() // 2))
    screen.blit(planet3_image, (planet3_x - planet3_image.get_width() // 2, planet3_y - planet3_image.get_height() // 2))
    screen.blit(planet4_image, (planet4_x - planet4_image.get_width() // 2, planet4_y - planet4_image.get_height() // 2))

    pygame.draw.rect(screen, shop_button_color, shop_button_rect, border_radius=shop_button_corner_radius)
    text1 = font.render("Магазин", True, text_color)
    text1_rect = text1.get_rect(center=shop_button_rect.center)
    screen.blit(text1, text1_rect)

    pygame.draw.rect(screen, help_button_color, help_button_rect, border_radius=help_button_corner_radius)
    screen.blit(help_button_icon, (help_button_rect.centerx - help_button_icon.get_width() // 2, help_button_rect.centery - help_button_icon.get_height() // 2))

    pygame.draw.rect(screen, setting_button_color, setting_button_rect, border_radius=setting_button_corner_radius)
    screen.blit(setting_button_icon, (setting_button_rect.centerx - setting_button_icon.get_width() // 2, setting_button_rect.centery - setting_button_icon.get_height() // 2))

    # Отрисовка орбит
    pygame.draw.ellipse(screen, (255, 255, 255), orbit_1, 1)
    pygame.draw.ellipse(screen, (255, 255, 255), orbit_2, 1)
    pygame.draw.ellipse(screen, (255, 255, 255), orbit_3, 1)
    pygame.draw.ellipse(screen, (255, 255, 255), orbit_4, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
