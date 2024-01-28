import pygame
import math

pygame.init()
width, height = 900, 600
screen = pygame.display.set_mode((width, height))

background_image = pygame.image.load("data/background.png")

# библиотека цветов
vivid_orange = (255, 194, 38)
white = (255, 255, 255)
text_color = (0, 2, 18)

shop_button_rect = pygame.Rect(30, 20, 200, 65)
shop_button_color = vivid_orange
shop_button_corner_radius = 10

help_button_rect = pygame.Rect(730, 20, 65, 65)
help_button_color = vivid_orange
help_button_corner_radius = 10
help_button_icon = pygame.image.load("data/help.png")

setting_button_rect = pygame.Rect(810, 20, 65, 65)
setting_button_color = vivid_orange
setting_button_corner_radius = 10
setting_button_icon = pygame.image.load("data/setting.png")

money = 0
money_color = vivid_orange
money_border_icon = pygame.image.load("data/border.png")

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

click_button_rect = pygame.Rect(715, 420, 160, 160)
click_button_color = vivid_orange
click_button_corner_radius = click_button_rect.width // 2

font_black = pygame.font.SysFont(None, 32)
font_vivid_orange = pygame.font.SysFont(None, 38)


def draw_task(color, y_coord, value, draw, length, speed):
    global score
    if draw and length < 200:
        length += speed
    elif length >= 200:
        draw = False
        length = 0
        score += value
    task = pygame.draw.circle(screen, color, (30, y_coord), 20, 5)
    value_text = font_black.render(str(round(value, 2)), True, text_color)
    screen.blit(value_text, (16, y_coord - 10))
    return task, length, draw


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if event.type == pygame.MOUSEBUTTONDOWN:
        #    if task1.collidepoint(event.pos):
        #        draw_green = True

    screen.blit(background_image, (0, 0))

    # Отрисовка орбит
    pygame.draw.ellipse(screen, white, orbit_1, 1)
    pygame.draw.ellipse(screen, white, orbit_2, 1)
    pygame.draw.ellipse(screen, white, orbit_3, 1)
    pygame.draw.ellipse(screen, white, orbit_4, 1)

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
    text1 = font_black.render("Магазин", True, text_color)
    text1_rect = text1.get_rect(center=shop_button_rect.center)
    screen.blit(text1, text1_rect)

    pygame.draw.rect(screen, help_button_color, help_button_rect, border_radius=help_button_corner_radius)
    screen.blit(help_button_icon, (help_button_rect.centerx - help_button_icon.get_width() // 2, help_button_rect.centery - help_button_icon.get_height() // 2))

    pygame.draw.rect(screen, setting_button_color, setting_button_rect, border_radius=setting_button_corner_radius)
    screen.blit(setting_button_icon, (setting_button_rect.centerx - setting_button_icon.get_width() // 2, setting_button_rect.centery - setting_button_icon.get_height() // 2))

    # Отрисовка круглой кнопки "Клик"
    pygame.draw.circle(screen, click_button_color, click_button_rect.center, click_button_corner_radius)
    text_click = font_black.render("Клик", True, text_color)
    text_click_rect = text_click.get_rect(center=click_button_rect.center)
    screen.blit(text_click, text_click_rect)

    # отрисовка счёта
    screen.blit(money_border_icon, (30, height - 140))
    text_money = font_vivid_orange.render("Ваш баланс:", True, vivid_orange)
    screen.blit(text_money, (55, height - 115))
    display_score = font_vivid_orange.render(str(round(money, 2)), True, vivid_orange)
    screen.blit(display_score, (55, height - 75))

    # функционал
    # task1, green_length, draw_green = draw_task(vivid_orange, 50, green_value, draw_green, green_length, green_speed)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
