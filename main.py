import os
import sys
import pygame
import math
import sqlite3
import pickle


def is_first_time():
    db_path = "player_data.db"
    return not os.path.exists(db_path)


def enter_game(player_id):
    if not is_first_time():
        player_db = PlayerDatabase()
        loaded_data = player_db.load_player_data(player_id)
        money, increment, increment_click, shop_data = loaded_data
        game_state.set_money(money)
        game_state.set_increment(increment)
        game_state.set_increment_click(increment_click)


def exit_game():
    player_db = PlayerDatabase()
    player_id = 1
    money = game_state.get_money()
    increment = game_state.get_increment()
    increment_click = game_state.get_increment_click()
    shop_data = game_state.get_shop()
    player_db.save_player_data(player_id, money, increment, increment_click, shop_data)
    print(money)

    pygame.quit()
    sys.exit()


# Класс для хранения данных игрока и работы с базой данных
class PlayerDatabase:
    def __init__(self, db_path="player_data.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                money REAL,
                increment REAL,
                increment_click REAL,
                shop_data BLOB
            )
        ''')
        self.conn.commit()

    def save_player_data(self, player_id, money, increment, increment_click, shop_data):
        serialized_shop_data = pickle.dumps(shop_data)
        self.cursor.execute('''
            INSERT OR REPLACE INTO players (id, money, increment, increment_click, shop_data)
            VALUES (?, ?, ?, ?, ?)
        ''', (player_id, money, increment, increment_click, serialized_shop_data))
        self.conn.commit()

    def load_player_data(self, player_id):
        query = "SELECT * FROM players WHERE id = ?;"
        self.cursor.execute(query, (player_id,))
        data = self.cursor.fetchone()
        if data:
            player_id, money, increment, increment_click, serialized_shop_data = data
            shop_data = pickle.loads(serialized_shop_data)
            return money, increment, increment_click, shop_data
        else:
            return None


pygame.init()
width, height = 900, 600
screen = pygame.display.set_mode((width, height))

background_image = pygame.image.load("data/background.png")
vivid_orange = (255, 194, 38)
white = (255, 255, 255)
space_color = (0, 2, 18)
dark_grey = (70, 70, 70)

font1 = pygame.sysfont.SysFont(None, 24)
font2 = pygame.sysfont.SysFont(None, 28)
font3 = pygame.sysfont.SysFont(None, 32)
font4 = pygame.sysfont.SysFont(None, 36)
font5 = pygame.sysfont.SysFont(None, 42)


def draw_image(name, coords):
    image = pygame.image.load('data/' + name)
    screen.blit(image, coords)


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
        self.selected_planet = None
        self.money = 0
        self.increment_click = 1
        self.increment = 0
        self.money_update_interval = 1000
        self.last_money_update_time = pygame.time.get_ticks()
        self.shop = Shop()

    def set_shop(self, shop):
        self.shop = shop

    def get_shop(self):
        return self.shop

    def set_money(self, new_money):
        self.money = new_money

    def get_money(self):
        return self.money

    def update_money(self, multiplier, add):
        if add:
            self.money += self.increment_click * multiplier
        else:
            self.money += multiplier

    def set_increment(self, new_increment):
        self.increment = new_increment

    def get_increment(self):
        return self.increment

    def update_increment(self, additional):
        self.increment += additional

    def auto_update_money(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_money_update_time >= self.money_update_interval:
            self.update_money(self.increment, 0)
            self.last_money_update_time = current_time

    def set_increment_click(self, new_increment_click):
        self.increment_click = new_increment_click

    def get_increment_click(self):
        return self.increment_click

    def update_increment_click(self, additional):
        self.increment_click += additional

    def set_current_state(self, state):
        self.current_state = state

    def get_selected_planet(self):
        return self.selected_planet

    def switch_to_planet_screen(self, planet_id):
        self.selected_planet = planet_id
        global current_state, planets
        current_state = planets[planet_id]

    def set_click_state(self, state):
        self.current_state.set_click_state(state)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_state.shop_button_rect.collidepoint(event.pos):
                    return "shop"
                elif self.current_state.help_button_rect.collidepoint(event.pos):
                    return "instruction"
                elif self.current_state.settings_button_rect.collidepoint(event.pos):
                    return "settings"
                elif self.current_state.planet_1_rect.collidepoint(event.pos):
                    click_sound.play()
                    self.switch_to_planet_screen(0)
                elif self.current_state.planet_2_rect.collidepoint(event.pos):
                    click_sound.play()
                    self.switch_to_planet_screen(1)
                elif self.current_state.planet_3_rect.collidepoint(event.pos):
                    click_sound.play()
                    self.switch_to_planet_screen(2)
                elif self.current_state.planet_4_rect.collidepoint(event.pos):
                    click_sound.play()
                    self.switch_to_planet_screen(3)
                elif self.current_state.click_button_rect.collidepoint(event.pos):
                    click_sound.play()
                    self.set_click_state(True)
                    self.current_state.clicked_on_click_button = True

    def update(self):
        self.current_state.update()

    def draw(self, screen):
        self.current_state.draw(screen)


# настройки
class SettingsOverlay:
    def __init__(self):
        global font2
        self.font2 = font2
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
                    return "back2"
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
                return "back2"
        return None

    def draw(self, screen):

        exit_text = self.font2.render("Выйти из игры", True, space_color)
        exit_rect = exit_text.get_rect(center=self.exit_button.center)
        pygame.draw.rect(screen, vivid_orange, self.exit_button)
        screen.blit(exit_text, exit_rect)

        close_text = self.font2.render("Закрыть настройки", True, space_color)
        close_rect = close_text.get_rect(center=self.close_button.center)
        pygame.draw.rect(screen, vivid_orange, self.close_button)
        screen.blit(close_text, close_rect)

        volume_music_text = self.font2.render(f"Music Volume: {int(self.volume_music)}%", True, vivid_orange)
        volume_effects_text = self.font2.render(f"Effects Volume: {int(self.volume_effects)}%", True, vivid_orange)
        mute_music_text = self.font2.render(f"Mute Music: {self.mute_music}", True, vivid_orange)
        mute_effects_text = self.font2.render(f"Mute Effects: {self.mute_effects}", True, vivid_orange)

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
                return "back2"
        result = self.settings_overlay.handle_events(events)
        if result:
            if result == "back2":
                return "back2"
        return None

    def draw(self, screen):
        self.settings_overlay.draw(screen)


class GameScreenState:
    def __init__(self):

        self.shop_button_rect = pygame.Rect(25, 25, 200, 65)
        self.shop_button_icon = pygame.image.load("data/button_0.png")
        self.dark_shop_button_icon = pygame.image.load("data/button_1.png")

        self.help_button_rect = pygame.Rect(720, 25, 65, 65)
        self.help_button_icon = pygame.image.load("data/help.png")
        self.dark_help_button_icon = pygame.image.load("data/dark help.png")

        self.settings_button_rect = pygame.Rect(810, 25, 65, 65)
        self.settings_button_icon = pygame.image.load("data/settings.png")
        self.dark_settings_button_icon = pygame.image.load("data/dark settings.png")

        # self.money = 0
        self.money_border = pygame.Rect(25, 455, 250, 120)
        self.money_border_icon = pygame.image.load("data/border.png")

        self.click_button_rect = pygame.Rect(715, 415, 160, 160)
        self.click_button_icon = pygame.image.load("data/click.png")
        self.dark_click_button_icon = pygame.image.load("data/dark click.png")
        self.clicked_on_click_button = False

        self.star_rect = pygame.Rect(475, 270, 60, 60)
        self.star_image = pygame.image.load("data/star.png")

        self.draw_light_icons = [self.shop_button_icon, self.help_button_icon, self.settings_button_icon,
                                 self.money_border_icon, self.click_button_icon, self.star_image]
        self.draw_dark_icons = [self.dark_shop_button_icon, self.dark_help_button_icon, self.dark_settings_button_icon,
                                self.money_border_icon, self.dark_click_button_icon, self.star_image]
        self.draw_icons = [False for _ in range(len(self.draw_light_icons))]
        self.draw_rects = [self.shop_button_rect, self.help_button_rect, self.settings_button_rect, self.money_border,
                           self.click_button_rect, self.star_rect]

        global font3, font5
        self.font3 = font3
        self.font5 = font5

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

        self.selected_planet = None

    def switch_to_planet_screen(self, planet_id):
        self.current_state = PlanetScreenState(self, planet_id)

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

        a = 0
        for i, x in enumerate(self.draw_rects):
            if x.collidepoint(pygame.mouse.get_pos()):
                self.draw_icons = [0 for i in range(len(self.draw_rects))]
                self.draw_icons[i] = 1
                a = 1
                break
        if not a:
            self.draw_icons = [0 for i in range(len(self.draw_rects))]

    def handle_events(self, events):
        for event in events:
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
        # Отрисовка всего
        for i in range(len(self.draw_icons)):
            if self.draw_icons[i] == 0:
                screen.blit(self.draw_light_icons[i], self.draw_rects[i])
            else:
                screen.blit(self.draw_dark_icons[i], self.draw_rects[i])

        text_shop = self.font5.render("Магазин", True, space_color)
        text_shop_rect = text_shop.get_rect(center=self.shop_button_rect.center)
        screen.blit(text_shop, text_shop_rect)

        text_click = self.font5.render("Клик", True, space_color)
        text_click_rect = text_click.get_rect(center=self.click_button_rect.center)
        screen.blit(text_click, text_click_rect)

        # отрисовка счёта
        text_money = self.font5.render("Ваш баланс:", True, vivid_orange)
        screen.blit(text_money, (50, height - 127))
        display_score = self.font3.render(f"{round(game_state.get_money(), 2)} $", True, vivid_orange)
        screen.blit(display_score, (50, height - 92))
        display_inc_click = self.font3.render(f"{round(game_state.get_increment_click(), 2)} $/клик", True,
                                              vivid_orange)
        screen.blit(display_inc_click, (50, height - 62))
        display_inc = self.font3.render(f"{round(game_state.get_increment(), 2)} $/сек", True, vivid_orange)
        screen.blit(display_inc, (165, height - 62))

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

        global font1, font4
        self.font1 = font1
        self.font4 = font4

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text = self.font4.render(self.text, True, space_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def draw_info(self, screen):
        info_text = self.font1.render(self.info_text, True, white)
        text_rect = info_text.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
        screen.blit(info_text, text_rect)

    def handle_click(self, x, y):
        if self.rect.collidepoint(x, y) and self.action:
            self.action()


class InstructionScreen(Scene):
    def __init__(self):
        global font1
        self.font1 = font1
        self.close_button = pygame.Rect(350, 535, 200, 50)

        # Текст инструкции
        with open('instructions.txt', 'r', encoding='utf-8') as file:
            self.instruction_text = file.readlines()
        for i, x in enumerate(self.instruction_text):
            self.instruction_text[i] = self.instruction_text[i].replace('\n', '')

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.close_button.collidepoint(event.pos):
                    return "back2"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "back2"
        return None

    def draw(self, screen):
        # Отображение текста
        text_height = 20
        for line in self.instruction_text:
            text_render = self.font1.render(line, True, (255, 255, 255))
            screen.blit(text_render, (30, text_height))
            text_height += 20

        close_text = self.font1.render("Вернуться", True, space_color)
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
        self.purchased = False

    @property
    def click_value(self):
        return self.base_click_value * (self.level + 1)

    @property
    def cost(self):
        return self.base_cost * (self.level + 1)

    def upgrade(self):
        self.level += 1
        if self.level >= 5:
            self.purchased = True


# Класс для магазина
class Shop:
    def __init__(self):
        self.items = [
            ShopItem("Обсидиановая кирка", base_click_value=1, base_cost=10),
            ShopItem("Медная дрель", base_click_value=5, base_cost=20),
            ShopItem("Метановый газовик", base_click_value=10, base_cost=50),
            ShopItem("Аметистовый экскаватор", base_click_value=20, base_cost=100),
            # Добавьте другие предметы магазина по аналогии
        ]
        self.money = 0
        self.max_level = 5

    def handle_click(self):
        for item in self.items:
            self.money += item.click_value

    def purchase_item(self, item_index):
        shop = game_state.get_shop()
        item = self.items[item_index]
        if item.level < self.max_level and game_state.get_money() >= item.cost:
            game_state.update_money(-shop.items[item_index].cost * (item.level + 1), 0)
            game_state.update_increment_click(shop.items[item_index].click_value)
            item.upgrade()

    def get_shop_info(self):
        shop_info = []
        for item in self.items:
            status = "Куплено" if item.purchased else f"Стоимость: {item.cost} монет"
            info = [f"{item.name}: +{item.base_click_value} за клик за уровень,",
                    f"бонус предмета +{item.click_value - item.base_click_value}, {status}"]
            shop_info.append(info)
        return shop_info


# добавление магазина
class ShopScene(Scene):
    def __init__(self):
        super().__init__()
        self.shop = Shop()
        # self.shop_buttons = [
        #     Button(30, 100 + i * 70, 200, 50, vivid_orange, f"Купить {i + 1}", "",
        #            action=lambda i=i: self.purchase_item(i))
        #     for i in range(len(self.shop.items))
        # ]

        self.back_button_rect = pygame.Rect(25, 25, 65, 65)
        self.back_button_icon = pygame.image.load("data/back.png")
        self.dark_back_button_icon = pygame.image.load("data/dark back.png")

        self.help_button_rect = pygame.Rect(720, 25, 65, 65)
        self.help_button_icon = pygame.image.load("data/help.png")
        self.dark_help_button_icon = pygame.image.load("data/dark help.png")

        self.settings_button_rect = pygame.Rect(810, 25, 65, 65)
        self.settings_button_icon = pygame.image.load("data/settings.png")
        self.dark_settings_button_icon = pygame.image.load("data/dark settings.png")

        self.money_border = pygame.Rect(25, 455, 250, 120)
        self.money_border_icon = pygame.image.load("data/border.png")

        self.draw_light_icons = [self.help_button_icon, self.settings_button_icon,
                                 self.money_border_icon, self.back_button_icon]
        self.draw_dark_icons = [self.dark_help_button_icon, self.dark_settings_button_icon,
                                self.money_border_icon, self.dark_back_button_icon]
        self.draw_icons = [False for _ in range(len(self.draw_light_icons))]
        self.draw_rects = [self.help_button_rect, self.settings_button_rect, self.money_border,
                           self.back_button_rect]
        self.point_positions = [(25, 110), (25, 195), (25, 280), (25, 365)]
        self.point_images = [pygame.image.load(f"data/button_{i}.png") for i in range(2)]

        self.point_levels = [0, 0, 0, 0]
        self.p = self.point_levels.copy()

        self.rects = []
        for i in range(len(self.point_levels)):
            rect = pygame.Rect(self.point_positions[i][0], self.point_positions[i][1], 200, 65)
            self.rects.append(rect)

        # self.back_button_rect = pygame.Rect(25, 25, 65, 65)
        # self.exit_button = Button(30, 20, 200, 50, vivid_orange, "Назад", "Вернуться назад")

        self.shop_button_rect = pygame.Rect(25, 110, 200, 65)
        self.shop_button_icon = pygame.image.load("data/button_0.png")
        self.dark_shop_button_icon = pygame.image.load("data/button_1.png")

        global font3, font5
        self.font3 = font3
        self.font5 = font5

    def purchase_item(self, item_index):
        self.shop.purchase_item(item_index)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect.collidepoint(event.pos):
                    return "back1"
                if self.help_button_rect.collidepoint(event.pos):
                    return "instruction"
                if self.settings_button_rect.collidepoint(event.pos):
                    return "settings"
                else:
                    for i, x in enumerate(self.rects):
                        if x.collidepoint(pygame.mouse.get_pos()):
                            self.purchase_item(i)
                            break

    def update(self):
        a = 0
        for i, x in enumerate(self.draw_rects):
            if x.collidepoint(pygame.mouse.get_pos()):
                self.draw_icons = [0 for i in range(len(self.draw_rects))]
                self.draw_icons[i] = 1
                a = 1
                break
        if not a:
            self.draw_icons = [0 for i in range(len(self.draw_rects))]

        b = 0
        for i, x in enumerate(self.rects):
            if x.collidepoint(pygame.mouse.get_pos()):
                self.point_levels = self.p.copy()
                self.point_levels[i] += 1
                b = 1
                break
        if not b:
            self.point_levels = self.p.copy()

    def draw(self, screen):

        for i in range(len(self.draw_icons)):
            if self.draw_icons[i] == 0:
                screen.blit(self.draw_light_icons[i], self.draw_rects[i])
            else:
                screen.blit(self.draw_dark_icons[i], self.draw_rects[i])

        screen.blit(self.money_border_icon, self.money_border)
        text_money = self.font5.render("Ваш баланс:", True, vivid_orange)
        screen.blit(text_money, (50, height - 127))
        display_score = self.font3.render(f"{round(game_state.get_money(), 2)} $", True, vivid_orange)
        screen.blit(display_score, (50, height - 92))
        display_inc_click = self.font3.render(f"{round(game_state.get_increment_click(), 2)} $/клик", True,
                                              vivid_orange)
        screen.blit(display_inc_click, (50, height - 62))
        display_inc = self.font3.render(f"{round(game_state.get_increment(), 2)} $/сек", True, vivid_orange)
        screen.blit(display_inc, (165, height - 62))

        for i, position in enumerate(self.point_positions):
            screen.blit(self.point_images[self.point_levels[i]], self.rects[i].topleft)
            text_item = self.font5.render(f"Уровень {self.shop.items[i].level}", True, space_color)
            screen.blit(text_item, (50, 130 + i * 85))

        shop_info = self.shop.get_shop_info()
        for i, info in enumerate(shop_info):
            text1 = self.font3.render(info[0], True, vivid_orange)
            rect1 = text1.get_rect(midleft=(250, 130 + i * 85))
            screen.blit(text1, rect1)
            text2 = self.font3.render(info[1], True, vivid_orange)
            rect2 = text2.get_rect(midleft=(250, 160 + i * 85))
            screen.blit(text2, rect2)


class PlanetScreenState:
    def __init__(self, planet_id, current_state):
        self.planet_id = planet_id
        self.current_state = current_state
        self.planet_image = pygame.image.load(f"data/planet{planet_id}_big.png")
        self.orbit_rect = pygame.Rect(0, 0, 0, 0)
        global font3, font5
        self.font3 = font3
        self.font5 = font5

        self.money_update_interval = 1000
        self.last_money_update_time = pygame.time.get_ticks()

        self.back_button_rect = pygame.Rect(25, 115, 65, 65)
        self.back_button_icon = pygame.image.load("data/back.png")
        self.dark_back_button_icon = pygame.image.load("data/dark back.png")

        self.shop_button_rect = pygame.Rect(25, 25, 200, 65)
        self.shop_button_icon = pygame.image.load("data/button_0.png")
        self.dark_shop_button_icon = pygame.image.load("data/button_1.png")

        self.help_button_rect = pygame.Rect(720, 25, 65, 65)
        self.help_button_icon = pygame.image.load("data/help.png")
        self.dark_help_button_icon = pygame.image.load("data/dark help.png")

        self.settings_button_rect = pygame.Rect(810, 25, 65, 65)
        self.settings_button_icon = pygame.image.load("data/settings.png")
        self.dark_settings_button_icon = pygame.image.load("data/dark settings.png")

        self.money = 0
        self.money_border = pygame.Rect(25, 455, 250, 120)
        self.money_border_icon = pygame.image.load("data/border.png")

        self.click_button_rect = pygame.Rect(715, 415, 160, 160)
        self.click_button_icon = pygame.image.load("data/click.png")
        self.dark_click_button_icon = pygame.image.load("data/dark click.png")
        self.clicked_on_click_button = False

        self.draw_light_icons = [self.shop_button_icon, self.help_button_icon, self.settings_button_icon,
                                 self.money_border_icon, self.click_button_icon, self.back_button_icon]
        self.draw_dark_icons = [self.dark_shop_button_icon, self.dark_help_button_icon, self.dark_settings_button_icon,
                                self.money_border_icon, self.dark_click_button_icon, self.dark_back_button_icon]
        self.draw_icons = [False for _ in range(len(self.draw_light_icons))]
        self.draw_rects = [self.shop_button_rect, self.help_button_rect, self.settings_button_rect, self.money_border,
                           self.click_button_rect, self.back_button_rect]

        # Инициализация точек
        self.point_positions = [(410, 100), (480, 160), (550, 100)]
        if planet_id == 1:
            self.cost_point = 1500
            self.point_images = [pygame.image.load(f"data/icons/ametist_{i}.png") for i in range(8)]
        elif planet_id == 2:
            self.cost_point = 750
            self.point_images = [pygame.image.load(f"data/icons/metan_{i}.png") for i in range(8)]
        elif planet_id == 3:
            self.cost_point = 500
            self.point_images = [pygame.image.load(f"data/icons/copper_{i}.png") for i in range(8)]
        elif planet_id == 4:
            self.cost_point = 10
            self.point_images = [pygame.image.load(f"data/icons/obsidian_{i}.png") for i in range(8)]
        self.point_levels = [0, 0, 0]
        self.p = self.point_levels.copy()

        self.rects = []
        for i in range(len(self.point_levels)):
            rect = pygame.Rect(self.point_positions[i][0], self.point_positions[i][1], 70, 100)
            self.rects.append(rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.settings_button_rect.collidepoint(event.pos):
                    return "settings"
                elif self.back_button_rect.collidepoint(event.pos):
                    return "menu"
                elif self.shop_button_rect.collidepoint(event.pos):
                    return "shop"
                elif self.help_button_rect.collidepoint(event.pos):
                    return "instruction"
                elif self.click_button_rect.collidepoint(event.pos):
                    click_sound.play()
                    self.clicked_on_click_button = True
                else:
                    for i, x in enumerate(self.rects):
                        if x.collidepoint(pygame.mouse.get_pos()) and self.point_levels[i] <= 6:
                            self.update_increment(i)
                            break

    def update_increment(self, point_index):

        # Проверяем, хватает ли денег на обновление уровня точки
        if self.current_state.get_money() >= self.cost_point:
            # Получаем уровень точки
            self.point_levels[point_index] += 1
            self.p = self.point_levels.copy()
            inc = [1, 10, 50, 100]
            game_state.update_increment(inc[-self.planet_id])
            game_state.update_money(-self.cost_point, 0)

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

        a = 0
        for i, x in enumerate(self.draw_rects):
            if x.collidepoint(pygame.mouse.get_pos()):
                self.draw_icons = [0 for i in range(len(self.draw_rects))]
                self.draw_icons[i] = 1
                a = 1
                break
        if not a:
            self.draw_icons = [0 for i in range(len(self.draw_rects))]

        b = 0
        for i, x in enumerate(self.rects):
            if x.collidepoint(pygame.mouse.get_pos()):
                self.point_levels = self.p.copy()
                self.point_levels[i] += 1
                b = 1
                break
        if not b:
            self.point_levels = self.p.copy()

    def draw(self, screen):
        planet_x = 340
        planet_y = 125

        # Отрисовка планеты
        screen.blit(self.planet_image, (planet_x, planet_y))

        # Отрисовка всего
        for i in range(len(self.draw_icons)):
            if self.draw_icons[i] == 0:
                screen.blit(self.draw_light_icons[i], self.draw_rects[i])
            else:
                screen.blit(self.draw_dark_icons[i], self.draw_rects[i])

        text_shop = self.font5.render("Магазин", True, space_color)
        text_shop_rect = text_shop.get_rect(center=self.shop_button_rect.center)
        screen.blit(text_shop, text_shop_rect)

        text_click = self.font5.render("Клик", True, space_color)
        text_click_rect = text_click.get_rect(center=self.click_button_rect.center)
        screen.blit(text_click, text_click_rect)

        # Отрисовка счёта
        screen.blit(self.money_border_icon, self.money_border)
        text_money = self.font5.render("Ваш баланс:", True, vivid_orange)
        screen.blit(text_money, (50, height - 127))
        display_score = self.font3.render(f"{round(game_state.get_money(), 2)} $", True, vivid_orange)
        screen.blit(display_score, (50, height - 92))
        display_inc_click = self.font3.render(f"{round(game_state.get_increment_click(), 2)} $/клик", True,
                                              vivid_orange)
        screen.blit(display_inc_click, (50, height - 62))
        display_inc = self.font3.render(f"{round(game_state.get_increment(), 2)} $/сек", True, vivid_orange)
        screen.blit(display_inc, (165, height - 62))

        for i, position in enumerate(self.point_positions):
            screen.blit(self.point_images[self.point_levels[i]], self.rects[i].topleft)


game_state = GameState()
pygame.mixer.music.load("data/startrack.mp3")
pygame.mixer.music.set_volume(0.5)

pygame.mixer.init()
click_sound = pygame.mixer.Sound("data/button.wav")
click_sound.set_volume(0.5)
shop_menu = ShopScene()
instruction = InstructionScreen()
settings_menu = SettingsMenu()
clock = pygame.time.Clock()
current_state = game_state
game_state_prev = current_state
planet_1 = PlanetScreenState(1, current_state)
planet_2 = PlanetScreenState(2, current_state)
planet_3 = PlanetScreenState(3, current_state)
planet_4 = PlanetScreenState(4, current_state)
planets = [planet_1, planet_2, planet_3, planet_4]

running = True
p, t = game_state, game_state

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Обработка событий и переключение сцен
    result = current_state.handle_events(events)
    if result:
        click_sound.play()
        if result == "settings":
            p = current_state
            current_state = settings_menu
            game_state_prev = p
        elif result == "shop":
            t = current_state
            p = current_state
            current_state = shop_menu
            game_state_prev = p
        elif result == "instruction":
            p = current_state
            current_state = instruction
            game_state_prev = p
        elif result == "back":
            p = current_state
            current_state = game_state_prev
            game_state_prev = p
        elif result == "menu":
            p = current_state
            current_state = game_state
            game_state_prev = p
        elif result == "back1":
            current_state = t
        elif result == "back2":
            current_state = game_state_prev

    game_state.auto_update_money()
    current_state.update()

    if pygame.mixer.music.get_busy() == 0:
        pygame.mixer.music.play()

    screen.blit(background_image, (0, 0))
    current_state.draw(screen)

    pygame.event.pump()
    pygame.display.flip()
    clock.tick(60)

if __name__ == "__main__":
    enter_game(1)
    exit_game()
