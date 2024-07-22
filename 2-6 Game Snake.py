# Цель: создать игровое приложение с использованием языка программирования Python 
# и библиотеки Pygame, которые обеспечивают возможности разработки игр на основе 
# объектно-ориентированных принципов, поддержку изображений, анимации, управление 
# основным игровым объектом (Персонажем).

# Что нужно сделать:
# 1) Создать игровое поле
# 2) Создать игровой объект “Змейка”
# 3) Создать игровой объект “Яблоко”
# 4) Реализовать алгоритм добавления блоков к змейке в случае поедания яблока

import pygame
import random

# Инициализация игры
pygame.init()

# Параметры игрового поля
width = 800
height = 600
cell_size = 20
rows = height // cell_size
cols = width // cell_size

# Список цветов
white = (255, 255, 255)
green = (0, 128, 0)
red = (255, 0, 0)

# Класс игрового объекта "Змейка"
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(random.randint(0, cols-1) * cell_size, random.randint(0, rows-1) * cell_size)]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        cur_x, cur_y = self.get_head_position()
        if self.direction == pygame.K_UP:
            new_pos = (cur_x, cur_y - cell_size)
        elif self.direction == pygame.K_DOWN:
            new_pos = (cur_x, cur_y + cell_size)
        elif self.direction == pygame.K_LEFT:
            new_pos = (cur_x - cell_size, cur_y)
        elif self.direction == pygame.K_RIGHT:
            new_pos = (cur_x + cell_size, cur_y)
        self.positions.insert(0, new_pos)
        if len(self.positions) > self.length:
            self.positions.pop()

# Класс игрового объекта "Яблоко"
class Apple:
    def __init__(self):
        self.position = (random.randint(0, cols-1) * cell_size, random.randint(0, rows-1) * cell_size)

    def update_position(self):
        self.position = (random.randint(0, cols-1) * cell_size, random.randint(0, rows-1) * cell_size)

# Текст
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont(None, size)
    text = font.render(text, True, white)
    surface.blit(text, (x, y))

# Запуск окна игры и исходных компонентов
win = pygame.display.set_mode((width, height))
snake = Snake()
apple = Apple()
score = 0
clock = pygame.time.Clock()
speed = 3

# Старт игры
while True:
# Закрыть по крестику
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
# Движение змейки стрелками клавитуры
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != pygame.K_DOWN:
                snake.direction = pygame.K_UP 
            elif event.key == pygame.K_DOWN and snake.direction != pygame.K_UP:
                snake.direction = pygame.K_DOWN
            elif event.key == pygame.K_LEFT and snake.direction != pygame.K_RIGHT:
                snake.direction = pygame.K_LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != pygame.K_LEFT:
                snake.direction = pygame.K_RIGHT
# Длина змейки +1 за 1 яблоко = счёт +1. 3 яблока = скорость +1.
    snake.move()
    if snake.get_head_position() == apple.position:
        snake.length += 1
        score += 1
        if score % 3 == 0:
            speed += 1
        apple.update_position()
# Бесконечность игрового поля для змейки (появляется с противоположной стороны)
    if snake.get_head_position()[0] < 0: snake.positions[0] = (width - cell_size, snake.get_head_position()[1])
    if snake.get_head_position()[0] >= width: snake.positions[0] = (0, snake.get_head_position()[1])
    if snake.get_head_position()[1] < 0: snake.positions[0] = (snake.get_head_position()[0], height - cell_size)
    if snake.get_head_position()[1] >= height: snake.positions[0] = (snake.get_head_position()[0], 0)
# Если змейка "укусит" себя, то конец игры, надпись, закрытие окна.
    for i in range(1, len(snake.positions)):
        if snake.get_head_position() == snake.positions[i]:
            draw_text(win, "Game Over", 50, width//2 - 100, height//2 - 25)
            pygame.display.update()
            pygame.time.wait(7000)
            pygame.quit()
            quit()
# Текстовый подсчёт счёта и скорости на экране поля
    win.fill(green)
    for pos in snake.positions:
        pygame.draw.rect(win, white, (*pos, cell_size, cell_size))
    pygame.draw.rect(win, red, (*apple.position, cell_size, cell_size))
    draw_text(win, f"Score: {score} Speed(3А=+1): {speed}", 30, cell_size, cell_size)

    pygame.display.update()
    clock.tick(speed)