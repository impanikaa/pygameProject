import sys

import pygame
import math

pygame.init()
width, height = 900, 600
screen = pygame.display.set_mode((width, height))

running = True

money = 0

background_image = pygame.image.load("data/background.png")
vivid_orange = (255, 194, 38)
white = (255, 255, 255)
space_color = (0, 2, 18)
dark_grey = (70, 70, 70)


class Scene:
    def __init__(self):
        pass

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


class GameState:
    def __init__(self):
        self.current_state = GameScreenState()
        self.planet_screen_active = False
        self.selected_planet = None
        self.money = 0

    def get_money(self):
        return self.money

    def update_money(self, amount):
        self.money += amount

    def set_current_state(self, state):
        self.current_state = state

    def set_selected_planet(self, planet):
        self.selected_planet = planet

    def get_selected_planet(self):
        return self.selected_planet

    def switch_to_planet_screen(self, planet_id):
        self.current_state = PlanetScreenState(planet_id, self)
        self.planet_screen_active = True

    def set_click_state(self, state):
        self.current_state.set_click_state(state)

    # def switch_to_settings(self):

    def handle_events(self, events):
        for event in events:
            if self.planet_screen_active:
                pass
                # self.current_state.handle_events(event)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_state.shop_button_rect.collidepoint(event.pos):
                        # Добавьте здесь действия для нажатия на кнопку "Магазин"
                        return "shop"
                    elif self.current_state.help_button_rect.collidepoint(event.pos):
                        # Добавьте здесь действия для нажатия на кнопку "Помощь"
                        pass
                    elif self.current_state.setting_button_rect.collidepoint(event.pos):
                        # Добавьте здесь действия для нажатия на кнопку "Настройки"
                        return "settings"
                    elif self.current_state.planet_1_rect.collidepoint(event.pos):
                        self.set_selected_planet(1)
                        self.switch_to_planet_screen(1)
                    elif self.current_state.planet_2_rect.collidepoint(event.pos):
                        self.set_selected_planet(2)
                        self.switch_to_planet_screen(2)
                    elif self.current_state.planet_3_rect.collidepoint(event.pos):
                        self.set_selected_planet(3)
                        self.switch_to_planet_screen(3)
                    elif self.current_state.planet_4_rect.collidepoint(event.pos):
                        self.set_selected_planet(4)
                        self.switch_to_planet_screen(4)
                    elif self.current_state.click_button_rect.collidepoint(event.pos):
                        self.set_click_state(True)
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


# настройки
class SettingsOverlay:
    def __init__(self):
        self.font = pygame.font.Font(None, 28)
        self.volume_music = 50
        self.volume_effects = 50
        self.mute_music = False
        self.mute_effects = False
        self.exit_button = pygame.Rect(250, 354, 200, 50)
        self.close_button = pygame.Rect(500, 354, 200, 50)
        self.update_buttons()

    def update_buttons(self):
        self.volume_music_button = pygame.Rect(250, 155, 200, 50)
        self.volume_effects_button = pygame.Rect(250, 240, 200, 50)
        self.mute_music_button = pygame.Rect(500, 155, 200, 50)
        self.mute_effects_button = pygame.Rect(500, 240, 200, 50)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif self.close_button.collidepoint(event.pos):
                    return "close_settings"
                elif self.volume_music_button.collidepoint(event.pos):
                    self.volume_music = max(0, min(100, (
                            event.pos[0] - self.volume_music_button.x) / self.volume_music_button.width * 100))
                    self.mute_music = False
                elif self.volume_effects_button.collidepoint(event.pos):
                    self.volume_effects = max(0, min(100, (
                            event.pos[0] - self.volume_effects_button.x) / self.volume_effects_button.width * 100))
                    self.mute_effects = False
                elif self.mute_music_button.collidepoint(event.pos):
                    self.mute_music = not self.mute_music
                    self.volume_music = 0 if self.mute_music else 50
                elif self.mute_effects_button.collidepoint(event.pos):
                    self.mute_effects = not self.mute_effects
                    self.volume_effects = 0 if self.mute_effects else 50
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "close_settings"
        return None

    def draw(self, screen):

        exit_text = self.font.render("Выйти из игры", True, space_color)
        exit_rect = exit_text.get_rect(center=self.exit_button.center)
        pygame.draw.rect(screen, vivid_orange, self.exit_button)
        screen.blit(exit_text, exit_rect)

        close_text = self.font.render("Закрыть настройки", True, space_color)
        close_rect = close_text.get_rect(center=self.close_button.center)
        pygame.draw.rect(screen, vivid_orange, self.close_button)
        screen.blit(close_text, close_rect)

        volume_music_text = self.font.render(f"Music Volume: {int(self.volume_music)}%", True, vivid_orange)
        volume_effects_text = self.font.render(f"Effects Volume: {int(self.volume_effects)}%", True, vivid_orange)
        mute_music_text = self.font.render(f"Mute Music: {self.mute_music}", True, vivid_orange)
        mute_effects_text = self.font.render(f"Mute Effects: {self.mute_effects}", True, vivid_orange)

        pygame.draw.rect(screen, vivid_orange, self.volume_music_button, 2)
        pygame.draw.rect(screen, vivid_orange, self.volume_effects_button, 2)
        pygame.draw.rect(screen, vivid_orange, (self.volume_music_button.x, self.volume_music_button.y,
                                                self.volume_music_button.width * self.volume_music / 100,
                                                self.volume_music_button.height))
        pygame.draw.rect(screen, vivid_orange, (self.volume_effects_button.x, self.volume_effects_button.y,
                                                self.volume_effects_button.width * self.volume_effects / 100,
                                                self.volume_effects_button.height))

        pygame.draw.rect(screen, vivid_orange, self.mute_music_button, 2)
        pygame.draw.rect(screen, vivid_orange, self.mute_effects_button, 2)

        if self.mute_music:
            pygame.draw.rect(screen, vivid_orange, self.mute_music_button)
        if self.mute_effects:
            pygame.draw.rect(screen, vivid_orange, self.mute_effects_button)

        screen.blit(volume_music_text, (250, 130))
        screen.blit(volume_effects_text, (250, 215))
        screen.blit(mute_music_text, (500, 130))
        screen.blit(mute_effects_text, (500, 215))


class SettingsMenu(Scene):
    def __init__(self):
        super().__init__()
        self.settings_overlay = SettingsOverlay()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "close_settings"
        result = self.settings_overlay.handle_events(events)
        if result:
            if result == "close_settings":
                return "main_menu"
        return None

    def draw(self, screen):
        self.settings_overlay.draw(screen)


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
        self.current_state = PlanetScreenState(self, planet_id)
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
            game_state.update_money(self.money_click_increment)
            self.clicked_on_click_button = False

    def handle_events(self, events):
        for event in events:
            if self.planet_screen_active:
                self.current_state.handle_events(event)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.planet_1_rect.collidepoint(event.pos):
                        self.set_selected_planet(1)
                        self.switch_to_planet_screen(1)
                    elif self.planet_2_rect.collidepoint(event.pos):
                        self.set_selected_planet(2)
                        self.switch_to_planet_screen(2)
                    elif self.planet_3_rect.collidepoint(event.pos):
                        self.set_selected_planet(3)
                        self.switch_to_planet_screen(3)
                    elif self.planet_4_rect.collidepoint(event.pos):
                        self.set_selected_planet(4)
                        self.switch_to_planet_screen(4)
                    elif self.click_button_rect.collidepoint(event.pos):
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
        text1 = self.font_black.render("Магазин", True, space_color)
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
        text_click = pygame.font.SysFont(None, 32).render("Клик", True, space_color)
        text_click_rect = text_click.get_rect(center=self.click_button_rect.center)
        screen.blit(text_click, text_click_rect)

        # отрисовка счёта
        screen.blit(self.money_border_icon, (30, height - 140))
        text_money = self.font_vivid_orange.render("Ваш баланс:", True, vivid_orange)
        screen.blit(text_money, (55, height - 115))
        display_score = self.font_vivid_orange.render(f"{round(game_state.get_money(), 2)} $", True, vivid_orange)
        screen.blit(display_score, (55, height - 75))

        # Обновление углов планет
        self.update()

        # Отрисовка орбит
        pygame.draw.ellipse(screen, white, self.orbit_1, 1)
        pygame.draw.ellipse(screen, white, self.orbit_2, 1)
        pygame.draw.ellipse(screen, white, self.orbit_3, 1)
        pygame.draw.ellipse(screen, white, self.orbit_4, 1)

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


        '''pygame.draw.rect(screen, white, self.planet_1_rect, 1)
        pygame.draw.rect(screen, white, self.planet_2_rect, 1)
        pygame.draw.rect(screen, white, self.planet_3_rect, 1)
        pygame.draw.rect(screen, white, self.planet_4_rect, 1)'''



# Класс для кнопок в игре
class Button:
    def __init__(self, x, y, width, height, color, text, info_text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.info_text = info_text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, space_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def draw_info(self, screen):
        font = pygame.font.Font(None, 24)
        info_text = font.render(self.info_text, True, white)
        text_rect = info_text.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
        screen.blit(info_text, text_rect)

    def handle_click(self, x, y):
        if self.rect.collidepoint(x, y) and self.action:
            self.action()


# Класс для предметов в магазине
class ShopItem:
    def __init__(self, name, base_click_value, base_cost):
        self.name = name
        self.base_click_value = base_click_value
        self.base_cost = base_cost
        self.level = 0

    @property
    def click_value(self):
        return self.base_click_value * (self.level + 1)

    @property
    def cost(self):
        return self.base_cost * (self.level + 1)

    def upgrade(self):
        self.level += 1


# Класс для магазина
class Shop:
    def __init__(self):
        self.items = [
            ShopItem("Upgrade 1", base_click_value=1, base_cost=10),
            ShopItem("Upgrade 2", base_click_value=5, base_cost=20),
            ShopItem("Upgrade 3", base_click_value=10, base_cost=50),
            ShopItem("Upgrade 4", base_click_value=20, base_cost=100),
            # Добавьте другие предметы магазина по аналогии
        ]
        self.money = 0

    def handle_click(self):
        for item in self.items:
            self.money += item.click_value

    def purchase_item(self, item_index):
        if 0 <= item_index < len(self.items):
            item = self.items[item_index]
            if self.money >= item.cost:
                self.money -= item.cost
                item.upgrade()

    def get_shop_info(self):
        shop_info = []
        for item in self.items:
            info = f"{item.name} (Уровень {item.level}): +{item.click_value} за клик, Стоимость: {item.cost} монет"
            shop_info.append(info)
        return shop_info


# добавление магазина
class ShopScene(Scene):
    def __init__(self):
        super().__init__()
        self.shop = Shop()
        self.shop_buttons = [
            Button(50, 90 + i * 70, 200, 50, vivid_orange, f"Купить {i+1}", "", action=lambda i=i: self.purchase_item(i))
            for i in range(len(self.shop.items))
        ]
        self.exit_button = Button(50, 20, 200, 50, vivid_orange, "Назад", "Вернуться на главный экран", action=self.go_back)

        self.money_color = vivid_orange
        self.money_border_icon = pygame.image.load("data/border.png")

        self.font = pygame.font.SysFont(None, 38)

    def purchase_item(self, item_index):
        self.shop.purchase_item(item_index)

    def go_back(self):
        global current_scene
        current_scene = game_state

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for button in self.shop_buttons:
                    button.handle_click(x, y)
                self.exit_button.handle_click(x, y)

    def draw(self, screen):
        # screen.fill(space_color)
        self.exit_button.draw(screen)
        self.exit_button.draw_info(screen)
        global money

        screen.blit(self.money_border_icon, (30, height - 140))
        text_money = self.font.render("Ваш баланс:", True, vivid_orange)
        screen.blit(text_money, (55, height - 115))
        display_score = self.font.render(f"{round(money, 2)} $", True, vivid_orange)
        screen.blit(display_score, (55, height - 75))

        for button in self.shop_buttons:
            button.draw(screen)
            button.draw_info(screen)

        shop_info = self.shop.get_shop_info()
        for i, info in enumerate(shop_info):
            text = self.font.render(info, True, white)
            rect = text.get_rect(midleft=(300, 50 + i * 70))
            screen.blit(text, rect)


class PlanetScreenState:
    def __init__(self, planet_id, current_state):
        self.planet_id = planet_id
        self.game_state = current_state
        self.planet_image = pygame.image.load(f"data/planet{planet_id}_big.png")
        self.orbit_rect = pygame.Rect(0, 0, 0, 0)

        # Кнопки и счет
        self.money = 0
        self.money_color = vivid_orange
        self.money_border_icon = pygame.image.load("data/border.png")

        self.money_update_interval = 1000
        self.last_money_update_time = pygame.time.get_ticks()
        self.money_click_increment = 1

        self.font_black = pygame.font.SysFont(None, 32)
        self.font_vivid_orange = pygame.font.SysFont(None, 38)

        self.shop_button_rect = pygame.Rect(110, 20, 200, 65)
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

        self.click_button_rect = pygame.Rect(715, 420, 160, 160)
        self.click_button_color = vivid_orange
        self.click_button_corner_radius = self.click_button_rect.width // 2
        self.clicked_on_click_button = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.click_button_rect.collidepoint(event.pos):
                    print("Кнопка 'Клик' была нажата")
                    self.clicked_on_click_button = True
                elif self.game_state.setting_button_rect.collidepoint(event.pos):
                    return "settings"
                elif self.click_button_rect.collidepoint(event.pos):
                    self.clicked_on_click_button = True

    def update(self):
        # Обновление времени
        current_time = pygame.time.get_ticks()

        # Обновление текста каждую секунду
        if current_time - self.last_money_update_time >= self.money_update_interval:
            self.last_money_update_time = current_time

        # Обновление money при клике
        if self.clicked_on_click_button:
            self.game_state.update_money(self.money_click_increment)
            self.clicked_on_click_button = False

    def draw(self, screen):
        planet_x = 340
        planet_y = 125

        screen.blit(self.planet_image, (planet_x, planet_y))

        pygame.draw.rect(screen, self.shop_button_color, self.shop_button_rect,
                         border_radius=self.shop_button_corner_radius)
        text1 = self.font_black.render("Магазин", True, space_color)
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
        text_click = pygame.font.SysFont(None, 32).render("Клик", True, space_color)
        text_click_rect = text_click.get_rect(center=self.click_button_rect.center)
        screen.blit(text_click, text_click_rect)

        # Отрисовка счета
        screen.blit(self.money_border_icon, (30, height - 140))
        text_money = self.font_vivid_orange.render("Ваш баланс:", True, vivid_orange)
        screen.blit(text_money, (55, height - 115))
        display_score = self.font_vivid_orange.render(f"{round(game_state.get_money(), 2)} $", True, vivid_orange)
        screen.blit(display_score, (55, height - 75))


shop_menu = ShopScene()
game_state = GameState()
settings_menu = SettingsMenu()
clock = pygame.time.Clock()
current_scene = game_state

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Обработка событий и переключение сцен
    result = current_scene.handle_events(events)
    if result:
        if current_scene == game_state:
            if result == "settings":
                current_scene = settings_menu
            elif result == "shop":
                current_scene = shop_menu
        elif current_scene == settings_menu:
            if result == "main_menu" or result == "close_settings":
                current_scene = game_state

    current_scene.update()

    screen.blit(background_image, (0, 0))
    current_scene.draw(screen)

    pygame.event.pump()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
