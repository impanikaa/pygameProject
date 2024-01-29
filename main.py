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
        self.increment_click = 1
        self.increment = 0
        self.money_update_interval = 1000
        self.last_money_update_time = pygame.time.get_ticks()
        self.shop = Shop()

    def get_shop(self):
        return self.shop

    def get_money(self):
        return self.money

    def update_money(self, multiplier, add):
        if add:
            self.money += self.increment_click * multiplier
        else:
            self.money += multiplier

    def get_increment(self):
        return self.increment

    def update_increment(self, additional):
        self.increment += additional

    def auto_update_money(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_money_update_time >= self.money_update_interval:
            self.update_money(self.increment, 0)
            self.last_money_update_time = current_time

    def get_increment_click(self):
        return self.increment_click

    def update_increment_click(self, additional):
        self.increment_click += additional

    def set_current_state(self, state):
        self.current_state = state

    def set_selected_planet(self, planet):
        self.selected_planet = planet

    def get_selected_planet(self):
        return self.selected_planet

    def switch_to_planet_screen(self, planet_id):
        global current_state
        # self.current_state = PlanetScreenState(planet_id, self)
        # self.planet_screen_active = True
        if planet_id == 1:
            current_state = planet_1
        if planet_id == 2:
            current_state = planet_2
        if planet_id == 3:
            current_state = planet_3
        if planet_id == 4:
            current_state = planet_4

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
                        return "shop"
                    elif self.current_state.help_button_rect.collidepoint(event.pos):
                        return "instruction"
                    elif self.current_state.setting_button_rect.collidepoint(event.pos):
                        return "settings"
                    elif self.current_state.planet_1_rect.collidepoint(event.pos):
                        click_sound.play()
                        self.set_selected_planet(1)
                        self.switch_to_planet_screen(1)
                    elif self.current_state.planet_2_rect.collidepoint(event.pos):
                        click_sound.play()
                        self.set_selected_planet(2)
                        self.switch_to_planet_screen(2)
                    elif self.current_state.planet_3_rect.collidepoint(event.pos):
                        click_sound.play()
                        self.set_selected_planet(3)
                        self.switch_to_planet_screen(3)
                    elif self.current_state.planet_4_rect.collidepoint(event.pos):
                        click_sound.play()
                        self.set_selected_planet(4)
                        self.switch_to_planet_screen(4)
                    elif self.current_state.click_button_rect.collidepoint(event.pos):
                        click_sound.play()
                        self.set_click_state(True)
                        self.current_state.clicked_on_click_button = True

    def update(self):
        self.auto_update_money()
        if self.planet_screen_active:
            self.current_state.update()
        else:
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

    def update_music_volume(self):
        pygame.mixer.music.set_volume(self.volume_music / 100)

    def update_effects_volume(self):
        pygame.mixer.set_num_channels(8)  # Устанавливаем количество каналов
        for channel in pygame.mixer.Channel.get_busy():
            channel.set_volume(self.volume_effects / 100)

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
                    return "back"
                elif self.volume_music_button.collidepoint(event.pos):
                    click_sound.play()
                    self.volume_music = max(0, min(100, (
                            event.pos[0] - self.volume_music_button.x) / self.volume_music_button.width * 100))
                    self.mute_music = False
                elif self.volume_effects_button.collidepoint(event.pos):
                    click_sound.play()
                    self.volume_effects = max(0, min(100, (
                            event.pos[0] - self.volume_effects_button.x) / self.volume_effects_button.width * 100))
                    self.mute_effects = False
                elif self.mute_music_button.collidepoint(event.pos):
                    click_sound.play()
                    self.mute_music = not self.mute_music
                    self.volume_music = 0 if self.mute_music else 50
                elif self.mute_effects_button.collidepoint(event.pos):
                    click_sound.play()
                    self.mute_effects = not self.mute_effects
                    self.volume_effects = 0 if self.mute_effects else 50
                elif self.volume_music_button.collidepoint(event.pos):
                    click_sound.play()
                    self.volume_music = max(0, min(100, (
                            event.pos[0] - self.volume_music_button.x) / self.volume_music_button.width * 100))
                    self.update_music_volume()
                    self.mute_music = False
                elif self.volume_effects_button.collidepoint(event.pos):
                    click_sound.play()
                    self.volume_effects = max(0, min(100, (
                            event.pos[0] - self.volume_effects_button.x) / self.volume_effects_button.width * 100))
                    self.update_effects_volume()
                    self.mute_effects = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "back"
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

        if 0 == self.volume_music:
            pygame.mixer.music.set_volume(0.0)
        elif 10 >= self.volume_music > 0:
            pygame.mixer.music.set_volume(0.1)
        elif 20 >= self.volume_music > 10:
            pygame.mixer.music.set_volume(0.2)
        elif 30 >= self.volume_music > 20:
            pygame.mixer.music.set_volume(0.3)
        elif 40 >= self.volume_music > 30:
            pygame.mixer.music.set_volume(0.4)
        elif 50 >= self.volume_music > 40:
            pygame.mixer.music.set_volume(0.5)
        elif 60 >= self.volume_music > 50:
            pygame.mixer.music.set_volume(0.6)
        elif 70 >= self.volume_music > 60:
            pygame.mixer.music.set_volume(0.7)
        elif 80 >= self.volume_music > 70:
            pygame.mixer.music.set_volume(0.8)
        elif 90 >= self.volume_music > 80:
            pygame.mixer.music.set_volume(0.9)
        elif 100 >= self.volume_music > 90:
            pygame.mixer.music.set_volume(1.0)

        if 0 == self.volume_effects:
            click_sound.set_volume(0.0)
        elif 10 >= self.volume_effects > 0:
            click_sound.set_volume(0.1)
        elif 20 >= self.volume_effects > 10:
            click_sound.set_volume(0.2)
        elif 30 >= self.volume_effects > 20:
            click_sound.set_volume(0.3)
        elif 40 >= self.volume_effects > 30:
            click_sound.set_volume(0.4)
        elif 50 >= self.volume_effects > 40:
            click_sound.set_volume(0.5)
        elif 60 >= self.volume_effects > 50:
            click_sound.set_volume(0.6)
        elif 70 >= self.volume_effects > 60:
            click_sound.set_volume(0.7)
        elif 80 >= self.volume_effects > 70:
            click_sound.set_volume(0.8)
        elif 90 >= self.volume_effects > 80:
            click_sound.set_volume(0.9)
        elif 100 >= self.volume_effects > 90:
            click_sound.set_volume(1.0)

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
                return "back"
        result = self.settings_overlay.handle_events(events)
        if result:
            if result == "back":
                return "back"
        return None

    def draw(self, screen):
        self.settings_overlay.draw(screen)


class GameScreenState:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 32)
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
        self.star_image = pygame.image.load("data/star.png")

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
            game_state.update_money(1, 1)
            self.clicked_on_click_button = False

    def handle_events(self, events):
        for event in events:
            if self.planet_screen_active:
                self.current_state.handle_events(event)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.planet_1_rect.collidepoint(event.pos):
                        click_sound.play()
                        self.set_selected_planet(1)
                        self.switch_to_planet_screen(1)
                    elif self.planet_2_rect.collidepoint(event.pos):
                        click_sound.play()
                        self.set_selected_planet(2)
                        self.switch_to_planet_screen(2)
                    elif self.planet_3_rect.collidepoint(event.pos):
                        click_sound.play()
                        self.set_selected_planet(3)
                        self.switch_to_planet_screen(3)
                    elif self.planet_4_rect.collidepoint(event.pos):
                        click_sound.play()
                        self.set_selected_planet(4)
                        self.switch_to_planet_screen(4)
                    elif self.click_button_rect.collidepoint(event.pos):
                        click_sound.play()
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

        star_rect = self.star_image.get_rect(topleft=(475, 270))
        screen.blit(self.star_image, star_rect)

        # Отрисовка круглой кнопки "Клик"
        pygame.draw.circle(screen, self.click_button_color, self.click_button_rect.center,
                           self.click_button_corner_radius)
        text_click = pygame.font.SysFont(None, 32).render("Клик", True, space_color)
        text_click_rect = text_click.get_rect(center=self.click_button_rect.center)
        screen.blit(text_click, text_click_rect)

        # отрисовка счёта
        screen.blit(self.money_border_icon, (30, height - 140))
        text_money = self.font_vivid_orange.render("Ваш баланс:", True, vivid_orange)
        screen.blit(text_money, (55, height - 122))
        display_score = self.font.render(f"{round(game_state.get_money(), 2)} $", True, vivid_orange)
        screen.blit(display_score, (55, height - 87))
        display_inc_click = self.font.render(f"{round(game_state.get_increment_click(), 2)} $/клик", True, vivid_orange)
        screen.blit(display_inc_click, (55, height - 57))
        display_inc = self.font.render(f"{round(game_state.get_increment(), 2)} $/сек", True, vivid_orange)
        screen.blit(display_inc, (170, height - 57))

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


class InstructionScreen(Scene):
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)
        self.close_button = pygame.Rect(350, 535, 200, 50)

        # Текст инструкции
        self.instruction_text = [
            "Добро пожаловать в инкрементальную игру 'Космический Кликер'!",
            "",
            "Цель игры: Увеличивайте свой космический баланс, нажимая на кнопку 'Клик' и автоматизируя доход.",
            "Зарабатывайте монеты и развивайте свой космический мир.",
            "",
            "Основные шаги:",
            "1. Нажимайте на Кнопку 'Клик': Чем больше кликов, тем больше монет вы зарабатываете.",
            "   Прокачивайте этот процесс для увеличения дохода.",
            "2. Магазин и Улучшения: Посещайте магазин, чтобы улучшить свои навыки и получать больше ",
            "монет за каждый клик.",
            "   Разблокируйте новые возможности и ускорьте свой прогресс.",
            "3. Планеты и Ресурсы: Исследуйте различные планеты и собирайте ресурсы. На всех планетах ",
            "свои ресурсы - обсидиан, медь, метан, аметисты.",
            "   Чем дальше планет от звезды, тем шахты на ней эффективнее, но дороже. Улучшайте шахты ",
            "для увеличения дохода.",
            "4. Автоматизация: Разблокируйте возможность автоматического заработка. Постройте шахты, которые ",
            "будут приносить монеты даже в вашем отсутствии.",
            "5. Управляйте Ресурсами: Тщательно распределяйте ресурсы и принимайте стратегические решения ",
            "для оптимизации своей космической империи.",
            "",
            "Подсказка: ",
            "Чем дальше вы продвигаетесь, тем больше возможностей и улучшений становится доступными.",
            "Не забывайте инвестировать в то, что приносит наибольший доход.",
            "",
            "Приятного путешествия по космосу и удачи в достижении максимального космического баланса!"
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.close_button.collidepoint(event.pos):
                    return "back"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "back"
        return None

    def draw(self, screen):
        # Отображение текста
        text_height = 20
        for line in self.instruction_text:
            text_render = self.font.render(line, True, (255, 255, 255))
            screen.blit(text_render, (30, text_height))
            text_height += 20

        close_text = self.font.render("Вернуться", True, space_color)
        close_rect = close_text.get_rect(center=self.close_button.center)
        pygame.draw.rect(screen, vivid_orange, self.close_button)
        screen.blit(close_text, close_rect)


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
        shop = game_state.get_shop()
        item = self.items[item_index]
        if game_state.get_money() >= item.cost:
            game_state.update_money(-shop.items[item_index].cost * (item.level + 1), 0)
            game_state.update_increment_click(shop.items[item_index].click_value)
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
            Button(30, 100 + i * 70, 200, 50, vivid_orange, f"Купить {i + 1}", "",
                   action=lambda i=i: self.purchase_item(i))
            for i in range(len(self.shop.items))
        ]
        self.return_button_rect = pygame.Rect(30, 20, 200, 50)
        self.exit_button = Button(30, 20, 200, 50, vivid_orange, "Назад", "Вернуться назад")

        self.money_color = vivid_orange
        self.money_border_icon = pygame.image.load("data/border.png")

        self.font = pygame.font.SysFont(None, 32)
        self.font_black = pygame.font.SysFont(None, 32)
        self.font_vivid_orange = pygame.font.SysFont(None, 38)

    def purchase_item(self, item_index):
        self.shop.purchase_item(item_index)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for button in self.shop_buttons:
                    button.handle_click(x, y)
                self.exit_button.handle_click(x, y)
                if self.return_button_rect.collidepoint(event.pos):
                    return "back"

    def draw(self, screen):
        # screen.fill(space_color)
        self.exit_button.draw(screen)
        self.exit_button.draw_info(screen)
        global money

        screen.blit(self.money_border_icon, (30, height - 140))
        text_money = self.font_vivid_orange.render("Ваш баланс:", True, vivid_orange)
        screen.blit(text_money, (55, height - 122))
        display_score = self.font.render(f"{round(game_state.get_money(), 2)} $", True, vivid_orange)
        screen.blit(display_score, (55, height - 87))
        display_inc_click = self.font.render(f"{round(game_state.get_increment_click(), 2)} $/клик", True, vivid_orange)
        screen.blit(display_inc_click, (55, height - 57))
        display_inc = self.font.render(f"{round(game_state.get_increment(), 2)} $/сек", True, vivid_orange)
        screen.blit(display_inc, (170, height - 57))

        for button in self.shop_buttons:
            button.draw(screen)
            button.draw_info(screen)

        shop_info = self.shop.get_shop_info()
        for i, info in enumerate(shop_info):
            text = self.font.render(info, True, white)
            rect = text.get_rect(midleft=(250, 120 + i * 70))
            screen.blit(text, rect)


class PlanetScreenState:
    def __init__(self, planet_id):
        self.planet_id = planet_id
        global current_state
        self.current_state = current_state
        self.planet_image = pygame.image.load(f"data/planet{planet_id}_big.png")
        self.orbit_rect = pygame.Rect(0, 0, 0, 0)
        self.font = pygame.font.SysFont(None, 32)

        # Кнопки и счет
        self.money = 0
        self.money_color = vivid_orange
        self.money_border_icon = pygame.image.load("data/border.png")

        self.money_update_interval = 1000
        self.last_money_update_time = pygame.time.get_ticks()

        self.font_black = pygame.font.SysFont(None, 32)
        self.font_vivid_orange = pygame.font.SysFont(None, 38)

        self.return_button_rect = pygame.Rect(30, 20, 65, 65)
        self.return_button_color = vivid_orange
        self.return_button_corner_radius = 10
        self.return_button_icon = pygame.image.load("data/back.png")

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

        # Инициализация точек
        self.point_positions = [(410, 100), (480, 160), (550, 100)]
        if planet_id == 1:
            self.cost_point = 1500
            self.point_images = [pygame.image.load(f"data/icons/ametist_{i + 1}.png") for i in range(6)]
        elif planet_id == 2:
            self.cost_point = 750
            self.point_images = [pygame.image.load(f"data/icons/metan_{i + 1}.png") for i in range(6)]
        elif planet_id == 3:
            self.cost_point = 500
            self.point_images = [pygame.image.load(f"data/icons/copper_{i + 1}.png") for i in range(6)]
        elif planet_id == 4:
            self.cost_point = 10
            self.point_images = [pygame.image.load(f"data/icons/obsidian_{i + 1}.png") for i in range(6)]
        self.point_levels = [0, 0, 0]

        self.point_click_processed = [False] * len(self.point_positions)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, position in enumerate(self.point_positions):
                    rect = pygame.Rect(position[0], position[1], 70, 100)
                    if rect.collidepoint(event.pos) and not self.point_click_processed[i]:
                        click_sound.play()
                        self.update_increment(i)
                        buy = self.update_increment(i)
                        print(f"Clicked on point {i + 1}")
                        if buy:
                            self.point_click_processed[i] = True
                if self.click_button_rect.collidepoint(event.pos):
                    self.clicked_on_click_button = True
                elif self.setting_button_rect.collidepoint(event.pos):
                    return "settings"
                elif self.return_button_rect.collidepoint(event.pos):
                    return "menu"
                if self.shop_button_rect.collidepoint(event.pos):
                    return "shop"
                if self.help_button_rect.collidepoint(event.pos):
                    return "instruction"

    def update_increment(self, point_index):
        # Получаем уровень точки
        point_level = self.point_levels[point_index]

        # Проверяем, хватает ли денег на обновление уровня точки
        if game_state.get_money() >= self.cost_point:
            self.point_levels[point_index] += 1
            if self.planet_id == 4:
                self.current_state.update_increment(point_level * 1)
            elif self.planet_id == 3:
                self.current_state.update_increment(point_level * 10)
            elif self.planet_id == 2:
                self.current_state.update_increment(point_level * 50)
            elif self.planet_id == 1:
                self.current_state.update_increment(point_level * 100)
            game_state.update_money(-self.cost_point * (self.point_levels[point_index]), 0)
            print(f"Point {point_index} upgraded to level {self.point_levels[point_index]}")
            buy = True
        else:
            print("Not enough money to upgrade the point")
            buy = False
        return buy

    def update(self):
        # Обновление времени
        current_time = pygame.time.get_ticks()

        # Обновление текста каждую секунду
        if current_time - self.last_money_update_time >= self.money_update_interval:
            self.last_money_update_time = current_time

        # Обновление money при клике
        if self.clicked_on_click_button:
            self.current_state.update_money(1, 1)
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

        # Отрисовка кнопки "Назад"
        pygame.draw.rect(screen, self.return_button_color, self.return_button_rect,
                         border_radius=self.return_button_corner_radius)
        screen.blit(self.return_button_icon, (
            self.return_button_rect.centerx - self.return_button_icon.get_width() // 2,
            self.return_button_rect.centery - self.return_button_icon.get_height() // 2))

        # Отрисовка счета
        screen.blit(self.money_border_icon, (30, height - 140))
        text_money = self.font_vivid_orange.render("Ваш баланс:", True, vivid_orange)
        screen.blit(text_money, (55, height - 122))
        display_score = self.font.render(f"{round(game_state.get_money(), 2)} $", True, vivid_orange)
        screen.blit(display_score, (55, height - 87))
        display_inc_click = self.font.render(f"{round(game_state.get_increment_click(), 2)} $/клик", True, vivid_orange)
        screen.blit(display_inc_click, (55, height - 57))
        display_inc = self.font.render(f"{round(game_state.get_increment(), 2)} $/сек", True, vivid_orange)
        screen.blit(display_inc, (170, height - 57))

        for i, position in enumerate(self.point_positions):
            rect = pygame.Rect(position[0], position[1], 70, 100)
            if self.point_levels[i] == 0:
                screen.blit(self.point_images[i + 3], rect.topleft)
            else:
                screen.blit(self.point_images[i], rect.topleft)


pygame.mixer.music.load("data/startrack.mp3")
pygame.mixer.music.set_volume(0.5)  # Здесь 0.9 - это громкость от 0.0 до 1.0

pygame.mixer.init()
click_sound = pygame.mixer.Sound("data/button.wav")
click_sound.set_volume(0.5)

shop_menu = ShopScene()
instruction = InstructionScreen()
game_state = GameState()
settings_menu = SettingsMenu()
clock = pygame.time.Clock()
current_state = game_state
game_state_prev = current_state
planet_1 = PlanetScreenState(1)
planet_2 = PlanetScreenState(2)
planet_3 = PlanetScreenState(3)
planet_4 = PlanetScreenState(4)

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Обработка событий и переключение сцен
    result = current_state.handle_events(events)
    if result:
        if result == "settings":
            click_sound.play()
            p = current_state
            current_state = settings_menu
            game_state_prev = p
        elif result == "shop":
            click_sound.play()
            p = current_state
            current_state = shop_menu
            game_state_prev = p
        elif result == "instruction":
            click_sound.play()
            p = current_state
            current_state = instruction
            game_state_prev = p
        elif result == "back":
            click_sound.play()
            p = current_state
            current_state = game_state_prev
            game_state_prev = p
        elif result == "menu":
            click_sound.play()
            p = current_state
            current_state = game_state
            game_state_prev = p

    current_state.update()

    if pygame.mixer.music.get_busy() == 0:
        pygame.mixer.music.play()

    screen.blit(background_image, (0, 0))
    current_state.draw(screen)

    pygame.event.pump()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
