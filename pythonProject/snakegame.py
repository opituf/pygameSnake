import pygame
import time
import random
import os

# Инициализация Pygame
pygame.init()

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

# Высота панели для отображения счёта и рекорда
panel_height = 50

# Создание окна
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка')

# Часы для контроля скорости змейки
clock = pygame.time.Clock()

snake_block = 10

# Шрифты
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
menu_font = pygame.font.SysFont("comicsansms", 50)

# Файл для хранения рекорда
record_file = 'snake_record.txt'

def get_high_score():
    if os.path.exists(record_file):
        with open(record_file, 'r') as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0
    return 0

def save_high_score(score):
    with open(record_file, 'w') as file:
        file.write(str(score))

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def your_score(score, high_score):
    value = score_font.render(f"Ваш счёт: {score}", True, yellow)
    high_value = score_font.render(f"Рекорд: {high_score}", True, yellow)
    dis.blit(value, [10, 10])
    dis.blit(high_value, [dis_width - high_value.get_width() - 10, 10])

def draw_menu():
    dis.fill(blue)
    title = menu_font.render("Змейка", True, white)
    easy_text = font_style.render("Легко (30 очков)", True, white)
    medium_text = font_style.render("Средне (60 очков)", True, white)
    hard_text = font_style.render("Тяжело (100 очков)", True, white)

    dis.blit(title, [dis_width / 3, dis_height / 6])
    dis.blit(easy_text, [dis_width / 3, dis_height / 2 - 50])
    dis.blit(medium_text, [dis_width / 3, dis_height / 2])
    dis.blit(hard_text, [dis_width / 3, dis_height / 2 + 50])

    pygame.display.update()

def gameLoop(difficulty):
    game_over = False
    game_close = False
    win = False

    x1 = dis_width / 2
    y1 = panel_height + snake_block  # Начальная позиция ниже панели

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(panel_height, dis_height - snake_block) / 10.0) * 10.0

    high_score = get_high_score()

    snake_speed = {
        'easy': 10,
        'medium': 15,
        'hard': 20
    }[difficulty]

    win_condition = {
        'easy': 30,
        'medium': 60,
        'hard': 100
    }[difficulty]

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("Вы проиграли! Нажмите Q-Выйти или C-Играть снова", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        main_menu()

        while win == True:
            dis.fill(blue)
            message("Вы выиграли! Нажмите Q-Выйти или C-Играть снова", green)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        win = False
                    if event.key == pygame.K_c:
                        gameLoop(difficulty)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0

        # Проверка столкновения со стенками
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < panel_height:
            game_close = True
            if Length_of_snake - 1 > high_score:
                save_high_score(Length_of_snake - 1)
                high_score = Length_of_snake - 1

        x1 += x1_change
        y1 += y1_change

        # Проверка условия победы
        if Length_of_snake >= win_condition:
            win = True
            if Length_of_snake - 1 > high_score:
                save_high_score(Length_of_snake - 1)
                high_score = Length_of_snake - 1

        # Отрисовка панели для счёта и рекорда
        dis.fill(blue)
        pygame.draw.rect(dis, white, [0, 0, dis_width, panel_height])

        # Отрисовка змеи и еды
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Проверка столкновения с самой собой
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
                if Length_of_snake - 1 > high_score:
                    save_high_score(Length_of_snake - 1)
                    high_score = Length_of_snake - 1

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1, high_score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(panel_height, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

def main_menu():
    menu = True
    while menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if dis_width / 3 <= mouse_pos[0] <= dis_width / 3 + 200:
                    if dis_height / 2 - 50 <= mouse_pos[1] <= dis_height / 2 - 50 + 50:
                        gameLoop('easy')
                    elif dis_height / 2 <= mouse_pos[1] <= dis_height / 2 + 50:
                        gameLoop('medium')
                    elif dis_height / 2 + 50 <= mouse_pos[1] <= dis_height / 2 + 100:
                        gameLoop('hard')

main_menu()