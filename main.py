import pygame
import math

pygame.init()
width, height = 900, 600
screen = pygame.display.set_mode((width, height))

running = True

background_image = pygame.image.load("data/background.png")
vivid_orange = (255, 194, 38)
white = (255, 255, 255)
text_color = (0, 2, 18)

class GameState:
    def __init__(self):
        self.current_state = GameScreenState()
        self.planet_screen_active = False

    def switch_to_planet_screen(self):
        self.current_state = PlanetScreenState()
        self.planet_screen_active = True

    def handle_event(self, event):
        if self.planet_screen_active:
            self.current_state.handle_event(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_state.shop_button_rect.collidepoint(event.pos):
                    # Добавьте здесь действия для нажатия на кнопку "Магазин"
                    pass
                elif self.current_state.help_button_rect.collidepoint(event.pos):
                    # Добавьте здесь действия для нажатия на кнопку "Помощь"
                    pass
                elif self.current_state.setting_button_rect.collidepoint(event.pos):
                    # Добавьте здесь действия для нажатия на кнопку "Настройки"
                    pass
                elif self.current_state.click_button_rect.collidepoint(event.pos):
                    # Добавьте здесь действия для нажатия на кнопку "Клик"
                    pass

    def update(self):
        if self.planet_screen_active:
            self.current_state.update()
        else:
            # Добавьте логику обновления для главного экрана, если необходимо
            pass

    def draw(self, screen):
        if self.planet_screen_active:
            self.current_state.draw(screen)
        else:
            # Добавьте отрисовку для главного экрана, если необходимо
            self.current_state.draw(screen)

class GameScreenState:
    def __init__(self):
        self.shop_button_rect = pygame.Rect(30, 20, 200, 65)
        self.shop_button_color = vivid_orange
        self.shop_button_corner_radius = 10

        self.help_button_rect = pygame.Rect(730, 20, 65, 65)
        self.help_button_color = vivid_orange
        self.help_button_corner_radius = 10
        self.help_button_icon = pygame.image.load("data/help.png")

        self.setting_button_rect = pygame.Rect(810, 20, 65, 65)
        self.setting_button_color = vivid_orange
        self.setting_button_corner_radius = 10
        self.setting_button_icon = pygame.image.load("data/setting.png")

        self.money = 0
        self.money_color = vivid_orange
        self.money_border_icon = pygame.image.load("data/border.png")

        self.click_button_rect = pygame.Rect(715, 420, 160, 160)
        self.click_button_color = vivid_orange
        self.click_button_corner_radius = self.click_button_rect.width // 2

        self.font_black = pygame.font.SysFont(None, 32)
        self.font_vivid_orange = pygame.font.SysFont(None, 38)

        self.planet1_image = pygame.image.load("data/planet1.png")
        self.planet2_image = pygame.image.load("data/planet2.png")
        self.planet3_image = pygame.image.load("data/planet3.png")
        self.planet4_image = pygame.image.load("data/planet4.png")

        self.orbit_1 = pygame.Rect(280, 75, 450, 450)
        self.orbit_2 = pygame.Rect(340, 135, 330, 330)
        self.orbit_3 = pygame.Rect(390, 185, 230, 230)
        self.orbit_4 = pygame.Rect(440, 235, 130, 130)

        self.angular_speed_1 = 0.00007
        self.angular_speed_2 = 0.0002
        self.angular_speed_3 = 0.00035
        self.angular_speed_4 = 0.0005

        # Исходные углы для планет
        self.angle_1 = 0
        self.angle_2 = 0
        self.angle_3 = 0
        self.angle_4 = 0

        # Установка начальных координат для планет
        self.update_planet_positions()

    def handle_event(self, event):
        pass  # Здесь вы можете добавить обработку событий, если это необходимо

    def update(self):
        # Обновление времени
        current_time = pygame.time.get_ticks()

        # Обновление углов планет
        self.angle_1 = current_time * self.angular_speed_1
        self.angle_2 = current_time * self.angular_speed_2
        self.angle_3 = current_time * self.angular_speed_3
        self.angle_4 = current_time * self.angular_speed_4

        # Обновление координат планет на орбитах
        self.update_planet_positions()

    def update_planet_positions(self):
        # Обновление координат планет на орбитах
        self.planet1_x = int(self.orbit_1.centerx + self.orbit_1.width / 2 * math.cos(self.angle_1))
        self.planet1_y = int(self.orbit_1.centery + self.orbit_1.height / 2 * math.sin(self.angle_1))

        self.planet2_x = int(self.orbit_2.centerx + self.orbit_2.width / 2 * math.cos(self.angle_2))
        self.planet2_y = int(self.orbit_2.centery + self.orbit_2.height / 2 * math.sin(self.angle_2))

        self.planet3_x = int(self.orbit_3.centerx + self.orbit_3.width / 2 * math.cos(self.angle_3))
        self.planet3_y = int(self.orbit_3.centery + self.orbit_3.height / 2 * math.sin(self.angle_3))

        self.planet4_x = int(self.orbit_4.centerx + self.orbit_4.width / 2 * math.cos(self.angle_4))
        self.planet4_y = int(self.orbit_4.centery + self.orbit_4.height / 2 * math.sin(self.angle_4))


    def draw(self, screen):
        pygame.draw.rect(screen, self.shop_button_color, self.shop_button_rect, border_radius=self.shop_button_corner_radius)
        text1 = self.font_black.render("Магазин", True, text_color)
        text1_rect = text1.get_rect(center=self.shop_button_rect.center)
        screen.blit(text1, text1_rect)

        pygame.draw.rect(screen, self.help_button_color, self.help_button_rect, border_radius=self.help_button_corner_radius)
        screen.blit(self.help_button_icon, (self.help_button_rect.centerx - self.help_button_icon.get_width() // 2, self.help_button_rect.centery - self.help_button_icon.get_height() // 2))

        pygame.draw.rect(screen, self.setting_button_color, self.setting_button_rect, border_radius=self.setting_button_corner_radius)
        screen.blit(self.setting_button_icon, (self.setting_button_rect.centerx - self.setting_button_icon.get_width() // 2, self.setting_button_rect.centery - self.setting_button_icon.get_height() // 2))

        # Отрисовка круглой кнопки "Клик"
        pygame.draw.circle(screen, self.click_button_color, self.click_button_rect.center, self.click_button_corner_radius)
        text_click = self.font_black.render("Клик", True, text_color)
        text_click_rect = text_click.get_rect(center=self.click_button_rect.center)
        screen.blit(text_click, text_click_rect)

        # отрисовка счёта
        screen.blit(self.money_border_icon, (30, height - 140))
        text_money = self.font_vivid_orange.render("Ваш баланс:", True, vivid_orange)
        screen.blit(text_money, (55, height - 115))
        display_score = self.font_vivid_orange.render(str(round(self.money, 2)), True, vivid_orange)
        screen.blit(display_score, (55, height - 75))

        # Отрисовка орбит
        pygame.draw.ellipse(screen, white, self.orbit_1, 1)
        pygame.draw.ellipse(screen, white, self.orbit_2, 1)
        pygame.draw.ellipse(screen, white, self.orbit_3, 1)
        pygame.draw.ellipse(screen, white, self.orbit_4, 1)

        # Обновление углов планет
        self.update()

        # Отрисовка планет
        screen.blit(self.planet1_image, (self.planet1_x - self.planet1_image.get_width() // 2, self.planet1_y - self.planet1_image.get_height() // 2))
        screen.blit(self.planet2_image, (self.planet2_x - self.planet2_image.get_width() // 2, self.planet2_y - self.planet2_image.get_height() // 2))
        screen.blit(self.planet3_image, (self.planet3_x - self.planet3_image.get_width() // 2, self.planet3_y - self.planet3_image.get_height() // 2))
        screen.blit(self.planet4_image, (self.planet4_x - self.planet4_image.get_width() // 2, self.planet4_y - self.planet4_image.get_height() // 2))


class PlanetScreenState:
    def __init__(self):
        # Добавьте здесь инициализацию для экрана с планетой
        self.planet_image = pygame.image.load("data/planet1.png")
        self.orbit_rect = pygame.Rect(280, 75, 450, 450)

    def handle_event(self, event):
        # Обработка событий для экрана с планетой
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.orbit_rect.collidepoint(event.pos):
                # Здесь вы можете выполнить действия, связанные с нажатием на планету
                pass

    def update(self):
        # Логика обновления для экрана с планетой
        pass

    def draw(self, screen):
        # Отрисовка для экрана с планетой
        pygame.draw.ellipse(screen, white, self.orbit_rect, 1)
        screen.blit(self.planet_image, (self.orbit_rect.centerx - self.planet_image.get_width() // 2, self.orbit_rect.centery - self.planet_image.get_height() // 2))

game = GameState()
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game.handle_event(event)

    # Обновление состояния игры
    game.update()

    screen.blit(background_image, (0, 0))

    # Отрисовка состояния игры
    game.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
