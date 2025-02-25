import pygame
import time
import random
import os

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Определение цветов
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Размеры экрана
dis_width = 800
dis_height = 600

# Размеры блока змеи по умолчанию
default_snake_block = 10

# Настройки сложности
difficulty_settings = {
    'easy': {
        'width': dis_width // 2,
        'height': dis_height // 2,
        'snake_block': default_snake_block * 2,
        'speed': 10,
        'record_file': 'easy_records.txt'
    },
    'medium': {
        'width': dis_width * 3 // 4,
        'height': dis_height * 3 // 4,
        'snake_block': default_snake_block * 1.5,
        'speed': 15,
        'record_file': 'medium_records.txt'
    },
    'hard': {
        'width': dis_width,
        'height': dis_height,
        'snake_block': default_snake_block,
        'speed': 20,
        'record_file': 'hard_records.txt'
    }
}

# Высота панели для отображения счета и рекорда
panel_height = 50

# Создание окна
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка')

# Часы для контроля скорости змеи
clock = pygame.time.Clock()

# Шрифты
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
menu_font = pygame.font.SysFont("comicsansms", 50)

# Глобальная переменная для уровня громкости
volume_level = 0.5

try:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(volume_level)  # Установка начального уровня громкости
    pygame.mixer.music.play(-1)  # -1 означает бесконечное воспроизведение
except pygame.error as e:
    print(f"Ошибка загрузки музыки: {e}")


# Загрузка изображений
def load_image(path, size):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except pygame.error as e:
        print(f"Ошибка загрузки изображения {path}: {e}")
        return pygame.Surface(size)


# Получение списка рекордов для конкретной сложности
def get_leaderboard(difficulty):
    record_file = difficulty_settings[difficulty]['record_file']
    if os.path.exists(record_file):
        with open(record_file, 'r') as file:
            lines = file.readlines()
            leaderboard = []
            for line in lines:
                name, score = line.strip().split(',')
                leaderboard.append((name, int(score)))
            return sorted(leaderboard, key=lambda x: x[1], reverse=True)
    return []


# Сохранение нового рекорда для конкретной сложности
def save_record(difficulty, name, score):
    record_file = difficulty_settings[difficulty]['record_file']
    with open(record_file, 'a') as file:
        file.write(f"{name},{score}\n")


# Получение счета лидера для конкретной сложности
def get_leader_score(difficulty):
    leaderboard = get_leaderboard(difficulty)
    if leaderboard:
        return leaderboard[0][1]
    return 0


def our_snake(snake_block, snake_list, direction, head_img, body_img):
    for i, segment in enumerate(snake_list):
        if i == 0:
            rotated_head = pygame.transform.rotate(head_img, direction)
            dis.blit(rotated_head, (segment[0], segment[1]))
        else:
            rotated_body = pygame.transform.rotate(body_img, direction)
            dis.blit(rotated_body, (segment[0], segment[1]))


def message(msg, color, width, height):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 6, height / 3])


def your_score(score, high_score, width):
    value = score_font.render(f"Ваш счёт: {score}", True, yellow)
    high_value = score_font.render(f"Рекорд: {high_score}", True, yellow)
    dis.blit(value, [10, 10])
    dis.blit(high_value, [width - high_value.get_width() - 10, 10])


# Ввод имени пользователя
def input_name():
    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN and name != "":
                    return name
        dis.fill(blue)
        text = font_style.render(f"Имя: {name}", True, white)
        dis.blit(text, [dis_width // 3, dis_height // 2])
        pygame.display.update()


def show_game_over_screen(score, difficulty):
    dis = pygame.display.set_mode((dis_width, dis_height))
    unnamed = True

    # Запрос имени игрока
    name = input_name()
    save_record(difficulty, name, score)
    # Получение таблицы лидеров
    leaderboard = get_leaderboard(difficulty)

    while unnamed:
        dis.fill(blue)
        message("Вы проиграли! Введите ваше имя:", red, dis_width, dis_height)
        pygame.display.update()
        if name != "":
            unnamed = False

    while True:
        # Отображение таблицы лидеров
        dis.fill(blue)
        message("Таблица лидеров:", white, dis_width, dis_height)
        y_position = dis_height // 2
        for i, (player_name, player_score) in enumerate(leaderboard[:5]):
            leaderboard_text = font_style.render(f"{i + 1}. {player_name} - {player_score}", True, white)
            dis.blit(leaderboard_text, [dis_width // 4, y_position])
            y_position += 40
        pygame.display.update()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Выход из игры
                    return False
                elif event.key == pygame.K_c:  # Продолжить игру
                    game_over_exit = True
                    return True


def show_victory_screen(score, difficulty):
    dis = pygame.display.set_mode((dis_width, dis_height))
    unnamed = True

    # Запрос имени игрока
    name = input_name()
    save_record(difficulty, name, score)
    # Получение таблицы лидеров
    leaderboard = get_leaderboard(difficulty)

    while unnamed:
        dis.fill(blue)
        message("Вы выиграли! Введите ваше имя:", red, dis_width, dis_height)
        pygame.display.update()
        if name != "":
            unnamed = False

    while True:
        # Отображение таблицы лидеров
        dis.fill(blue)
        message("Таблица лидеров:", white, dis_width, dis_height)
        y_position = dis_height // 2
        for i, (player_name, player_score) in enumerate(leaderboard[:5]):
            leaderboard_text = font_style.render(f"{i + 1}. {player_name} - {player_score}", True, white)
            dis.blit(leaderboard_text, [dis_width // 4, y_position])
            y_position += 40
        pygame.display.update()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Выход из игры
                    return False
                elif event.key == pygame.K_c:  # Продолжить игру
                    game_over_exit = True
                    return True


def draw_menu():
    global volume_level
    selected_difficulty = None

    while not selected_difficulty:
        dis.fill(blue)
        title = menu_font.render("Змейка", True, white)
        easy_text = font_style.render("Легко (E)", True, white)
        medium_text = font_style.render("Средне (M)", True, white)
        hard_text = font_style.render("Тяжело (H)", True, white)

        # Отображение управления громкостью
        draw_volume_controls(dis_width - 200, dis_height - 100)

        dis.blit(title, [dis_width / 3, dis_height / 6])
        dis.blit(easy_text, [dis_width / 3, dis_height / 2 - 50])
        dis.blit(medium_text, [dis_width / 3, dis_height / 2])
        dis.blit(hard_text, [dis_width / 3, dis_height / 2 + 50])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    selected_difficulty = 'easy'
                elif event.key == pygame.K_m:
                    selected_difficulty = 'medium'
                elif event.key == pygame.K_h:
                    selected_difficulty = 'hard'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if dis_width / 3 <= mouse_x <= dis_width / 3 + 150 and dis_height / 2 - 50 <= mouse_y <= dis_height / 2 - 20:
                    selected_difficulty = 'easy'
                elif dis_width / 3 <= mouse_x <= dis_width / 3 + 150 and dis_height / 2 <= mouse_y <= dis_height / 2 + 30:
                    selected_difficulty = 'medium'
                elif dis_width / 3 <= mouse_x <= dis_width / 3 + 150 and dis_height / 2 + 50 <= mouse_y <= dis_height / 2 + 80:
                    selected_difficulty = 'hard'
                else:
                    handle_volume_buttons(event.pos, dis_width - 200, dis_height - 100)

    return selected_difficulty


def draw_volume_controls(x, y):
    button_width = 30
    button_height = 30

    # Отображение надписи "Громкость"
    volume_text = font_style.render("Громкость", True, white)
    dis.blit(volume_text, [x, y - 40])

    # Отображение текущего уровня громкости
    volume_percent = int(volume_level * 100)
    percent_text = font_style.render(f"{volume_percent}%", True, white)
    dis.blit(percent_text, [x + 50, y])

    # Рисование кнопок "+/-"
    pygame.draw.rect(dis, green, [x, y, button_width, button_height])
    plus_text = font_style.render("+", True, black)
    dis.blit(plus_text, [x + 8, y + 5])

    pygame.draw.rect(dis, red, [x + 115, y, button_width, button_height])
    minus_text = font_style.render("-", True, black)
    dis.blit(minus_text, [x + 123, y + 5])


def handle_volume_buttons(mouse_pos, x, y):
    global volume_level
    button_width = 30
    button_height = 30

    # Проверка нажатия на кнопку "+"
    if x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height:
        volume_level = min(volume_level + 0.1, 1.0)
    # Проверка нажатия на кнопку "-"
    elif x + 115 <= mouse_pos[0] <= x + 115 + button_width and y <= mouse_pos[1] <= y + button_height:
        volume_level = max(volume_level - 0.1, 0.0)

    pygame.mixer.music.set_volume(volume_level)


class AppleAnimation:
    def __init__(self, x, y, frames, frame_delay):
        self.frames = frames
        self.current_frame = 0
        self.x = x
        self.y = y
        self.last_update_time = 0
        self.frame_delay = frame_delay

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_delay:
            self.last_update_time = current_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, surface):
        surface.blit(self.frames[self.current_frame], (self.x, self.y))


def gameLoop(difficulty):
    global volume_level
    game_over = False
    win = False

    # Применяем настройки для выбранной сложности
    dis_width_loc = difficulty_settings[difficulty]['width']
    dis_height_loc = difficulty_settings[difficulty]['height'] + panel_height
    snake_block = int(difficulty_settings[difficulty]['snake_block'])
    snake_speed = difficulty_settings[difficulty]['speed']

    # Загрузка спрайтов для яблока
    apple_frames = [load_image(f"apple_anim/apple{i}.png", (snake_block, snake_block)) for i in range(1, 5)]
    apple_animation = AppleAnimation(0, 0, apple_frames, 100)

    # Загрузка спрайтов для змеи
    snake_head_img = load_image("snake_head.png", (snake_block, snake_block))
    snake_body_img = load_image("snake_body.png", (snake_block, snake_block))

    # Создаем окно с новыми размерами
    dis = pygame.display.set_mode((dis_width_loc, dis_height_loc))
    pygame.display.set_caption('Змейка')

    x1 = dis_width_loc // 2
    y1 = panel_height + snake_block
    x1_change = 0
    y1_change = 0
    direction = 0
    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width_loc - snake_block) / snake_block) * snake_block
    foody = round(
        random.randrange(panel_height, dis_height_loc - panel_height - snake_block) / snake_block) * snake_block

    high_score = get_leader_score(difficulty)
    win_condition = {'easy': 30, 'medium': 60, 'hard': 100}[difficulty]

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                    direction = 180
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                    direction = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 90
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0
                    direction = 270

        x1 += x1_change
        y1 += y1_change

        # Проверка выхода за границы поля
        if x1 >= dis_width_loc or x1 < 0 or y1 >= dis_height_loc or y1 < panel_height:
            game_over = not show_game_over_screen(Length_of_snake - 1, difficulty)
            if not game_over:
                return gameLoop(difficulty)

        snake_Head = [x1, y1]
        if snake_Head in snake_List[:-1]:
            game_over = not show_game_over_screen(Length_of_snake - 1, difficulty)
            if not game_over:
                return gameLoop(difficulty)

        snake_List.insert(0, snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[-1]

        if Length_of_snake >= win_condition:
            win = not show_victory_screen(Length_of_snake - 1, difficulty)
            if not win:
                return gameLoop(difficulty)

        dis.fill(blue)
        pygame.draw.rect(dis, white, [0, 0, dis_width_loc, panel_height])

        our_snake(snake_block, snake_List, direction, snake_head_img, snake_body_img)
        apple_animation.x = foodx
        apple_animation.y = foody
        apple_animation.update()
        apple_animation.draw(dis)
        your_score(Length_of_snake - 1, high_score, dis_width_loc)
        pygame.display.update()

        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = round(random.randrange(0, dis_width_loc - snake_block) / snake_block) * snake_block
            foody = round(
                random.randrange(panel_height, dis_height_loc - panel_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


if __name__ == "__main__":
    selected_difficulty = draw_menu()
    gameLoop(selected_difficulty)
