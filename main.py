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
        self.selected_planet = None

    def set_current_state(self, state):
        self.current_state = state

    def set_selected_planet(self, planet):
        self.selected_planet = planet

    def get_selected_planet(self):
        return self.selected_planet

    def switch_to_planet_screen(self, planet_id):
        self.current_state = PlanetScreenState(planet_id)
        self.planet_screen_active = True

    def set_click_state(self, state):
        self.current_state.set_click_state(state)

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
                elif self.current_state.planet_1_rect.collidepoint(event.pos):
                    self.set_selected_planet(1)
                    self.current_state.switch_to_planet_screen(1)
                elif self.current_state.planet_2_rect.collidepoint(event.pos):
                    self.set_selected_planet(2)
                    self.current_state.switch_to_planet_screen(2)
                elif self.current_state.planet_3_rect.collidepoint(event.pos):
                    self.set_selected_planet(3)
                    self.current_state.switch_to_planet_screen(3)
                elif self.current_state.planet_4_rect.collidepoint(event.pos):
                    self.set_selected_planet(4)
                    self.current_state.switch_to_planet_screen(4)
                elif self.current_state.click_button_rect.collidepoint(event.pos):
                    self.current_state.clicked_on_click_button = True

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
        self.clicked_on_click_button = False

        self.font_black = pygame.font.SysFont(None, 32)
        self.font_vivid_orange = pygame.font.SysFont(None, 38)

        self.planet_1_rect = pygame.Rect(0, 0, 60, 60)
        self.planet_2_rect = pygame.Rect(0, 0, 75, 75)
        self.planet_3_rect = pygame.Rect(0, 0, 55, 55)
        self.planet_4_rect = pygame.Rect(0, 0, 35, 35)

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

        self.money_update_interval = 1000
        self.last_money_update_time = pygame.time.get_ticks()
        self.money_click_increment = 1

        self.selected_planet = None

    def switch_to_planet_screen(self, planet_id):
        self.current_state = PlanetScreenState(planet_id)
        self.planet_screen_active = True

    def set_click_state(self, state):
        self.clicked_on_click_button = state

    def set_selected_planet(self, planet):
        self.selected_planet = planet

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

        # Обновление текста каждую секунду
        if current_time - self.last_money_update_time >= self.money_update_interval:
            self.last_money_update_time = current_time

        # Обновление money при клике
        if self.clicked_on_click_button:
            self.money += self.money_click_increment
            self.clicked_on_click_button = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.planet_1_rect.collidepoint(event.pos):
                print("Clicked on planet 1")
                self.switch_to_planet_screen(1)
            elif self.planet_2_rect.collidepoint(event.pos):
                print("Clicked on planet 2")
                self.switch_to_planet_screen(2)
            elif self.planet_3_rect.collidepoint(event.pos):
                print("Clicked on planet 3")
                self.switch_to_planet_screen(3)
            elif self.planet_4_rect.collidepoint(event.pos):
                print("Clicked on planet 4")
                self.switch_to_planet_screen(4)
            elif self.click_button_rect.collidepoint(event.pos):
                print("Clicked on click button")
                self.clicked_on_click_button = True

    def update_planet_positions(self):
        self.planet1_x = int(self.orbit_1.centerx + self.orbit_1.width / 2 * math.cos(self.angle_1))
        self.planet1_y = int(self.orbit_1.centery + self.orbit_1.height / 2 * math.sin(self.angle_1))
        self.planet_1_rect.center = (self.planet1_x, self.planet1_y)

        self.planet2_x = int(self.orbit_2.centerx + self.orbit_2.width / 2 * math.cos(self.angle_2))
        self.planet2_y = int(self.orbit_2.centery + self.orbit_2.height / 2 * math.sin(self.angle_2))
        self.planet_2_rect.center = (self.planet2_x, self.planet2_y)

        self.planet3_x = int(self.orbit_3.centerx + self.orbit_3.width / 2 * math.cos(self.angle_3))
        self.planet3_y = int(self.orbit_3.centery + self.orbit_3.height / 2 * math.sin(self.angle_3))
        self.planet_3_rect.center = (self.planet3_x, self.planet3_y)

        self.planet4_x = int(self.orbit_4.centerx + self.orbit_4.width / 2 * math.cos(self.angle_4))
        self.planet4_y = int(self.orbit_4.centery + self.orbit_4.height / 2 * math.sin(self.angle_4))
        self.planet_4_rect.center = (self.planet4_x, self.planet4_y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.shop_button_color, self.shop_button_rect,
                         border_radius=self.shop_button_corner_radius)
        text1 = self.font_black.render("Магазин", True, text_color)
        text1_rect = text1.get_rect(center=self.shop_button_rect.center)
        screen.blit(text1, text1_rect)

        pygame.draw.rect(screen, self.help_button_color, self.help_button_rect,
                         border_radius=self.help_button_corner_radius)
        screen.blit(self.help_button_icon, (self.help_button_rect.centerx - self.help_button_icon.get_width() // 2,
                                            self.help_button_rect.centery - self.help_button_icon.get_height() // 2))

        pygame.draw.rect(screen, self.setting_button_color, self.setting_button_rect,
                         border_radius=self.setting_button_corner_radius)
        screen.blit(self.setting_button_icon, (
            self.setting_button_rect.centerx - self.setting_button_icon.get_width() // 2,
            self.setting_button_rect.centery - self.setting_button_icon.get_height() // 2))

        # Отрисовка круглой кнопки "Клик"
        pygame.draw.circle(screen, self.click_button_color, self.click_button_rect.center,
                           self.click_button_corner_radius)
        text_click = pygame.font.SysFont(None, 32).render("Клик", True, text_color)
        text_click_rect = text_click.get_rect(center=self.click_button_rect.center)
        screen.blit(text_click, text_click_rect)

        # отрисовка счёта
        screen.blit(self.money_border_icon, (30, height - 140))
        text_money = self.font_vivid_orange.render("Ваш баланс:", True, vivid_orange)
        screen.blit(text_money, (55, height - 115))
        display_score = self.font_vivid_orange.render(f"{round(self.money, 2)} $", True, vivid_orange)
        screen.blit(display_score, (55, height - 75))

        # Обновление углов планет
        self.update()

        # Отрисовка планет


        screen.blit(self.planet1_image, (
            self.planet1_x - self.planet1_image.get_width() // 2,
            self.planet1_y - self.planet1_image.get_height() // 2))
        screen.blit(self.planet2_image, (
            self.planet2_x - self.planet2_image.get_width() // 2,
            self.planet2_y - self.planet2_image.get_height() // 2))
        screen.blit(self.planet3_image, (
            self.planet3_x - self.planet3_image.get_width() // 2,
            self.planet3_y - self.planet3_image.get_height() // 2))
        screen.blit(self.planet4_image, (
            self.planet4_x - self.planet4_image.get_width() // 2,
            self.planet4_y - self.planet4_image.get_height() // 2))

        # Отрисовка орбит
        pygame.draw.ellipse(screen, white, self.orbit_1, 1)
        pygame.draw.ellipse(screen, white, self.orbit_2, 1)
        pygame.draw.ellipse(screen, white, self.orbit_3, 1)
        pygame.draw.ellipse(screen, white, self.orbit_4, 1)

        pygame.draw.rect(screen, white, self.planet_1_rect, 1)
        pygame.draw.rect(screen, white, self.planet_2_rect, 1)
        pygame.draw.rect(screen, white, self.planet_3_rect, 1)
        pygame.draw.rect(screen, white, self.planet_4_rect, 1)


class PlanetScreenState:
    def __init__(self, planet_id):
        # Добавьте здесь инициализацию для экрана с планетой
        self.planet_id = planet_id
        self.planet_image = pygame.image.load(f"data/planet{planet_id}_big.png")
        self.orbit_rect = pygame.Rect(0, 0, 0, 0)  # Ваши координаты орбиты здесь

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

        # Определение координат для отображения текста
        text_x = 20  # Измените на необходимые вам координаты
        text_y = 20  # Измените на необходимые вам координаты

        # Отображение текста
        text = pygame.font.SysFont(None, 24).render(f"Планета {self.planet_id}", True, text_color)
        screen.blit(text, (text_x, text_y))

        # Отображение изображения планеты
        planet_x = 340  # Измените на необходимые вам координаты
        planet_y = 125  # Измените на необходимые вам координаты

        screen.blit(self.planet_image, (planet_x, planet_y))


game_state = GameState()
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        game_state.handle_event(event)

    game_state.update()

    screen.blit(background_image, (0, 0))
    game_state.draw(screen)

    pygame.event.pump()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()