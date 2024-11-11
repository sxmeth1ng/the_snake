"""Импортируемые библиотеки."""
from random import choice, randrange

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
START_BOARD = 0

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

ALL_DIRECTION = (UP, DOWN, LEFT, RIGHT)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Центр игрового поля :

CENTER_OF_BOARD = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс для создания игровых объектов."""

    def __init__(self, color=None):
        """Конструктор класса.

        С заданными по умолчанию позицией объекта и его цветом.
        """
        self.position = CENTER_OF_BOARD
        self.body_color = color

    def draw(self):
        """Пустой метод для его дальнейшего переделывания."""


class Apple(GameObject):
    """Класс описывающий яблоко на игровом поле."""

    def __init__(self, color=APPLE_COLOR, busy_coordinates=(CENTER_OF_BOARD,)):
        """Конструктор класса, где задана позиция и поменян цвет объекта."""
        super().__init__(color)
        self.randomize_position(busy_coordinates)

    def draw(self):
        """Метод отрисовывающий объект на игровом поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, busy_place):
        """Метод генерирующий новую позицию объекта на поле."""
        while True:
            self.position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                             randrange(0, SCREEN_HEIGHT, GRID_SIZE))
            if self.position not in busy_place:
                break


class Snake(GameObject):
    """Класс описываюющий саму змею."""

    def __init__(self, color=SNAKE_COLOR):
        """Конструктор класса.

        В нём задаётся список состоящий из кортежей.
        Цвет змейки.
        """
        super().__init__(color)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.last = None

    def update_direction(self):
        """Метод меняющий направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод возвращающий позицию головы змеи."""
        return self.positions[0]

    def move(self):
        """Метод описывающий движение змейки."""
        direction_x, direction_y = self.direction
        x, y = self.get_head_position()
        head = (((x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH),
                ((y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT))
        self.positions.insert(0, head)
        self.last = (
            self.positions.pop()
            if self.length < len(self.positions)
            else None
        )

    def check_to_reset(self):
        """Метод проверяющий врезалась ли змейка сама в себя."""
        return self.get_head_position() in self.positions[2:]

    def draw(self):
        """Метод отрисовывающий змейку."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод прерывающий игру."""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice(ALL_DIRECTION)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция main, в ней запускается вся игра."""
    pg.init()
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.check_to_reset():
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
