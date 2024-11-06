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

    def __init__(self, color=None):
        """Конструктор класса, где задана позиция и поменян цвет объекта."""
        super().__init__(color)
        self.body_color = color

    def draw(self):
        """Метод отрисовывающий объект на игровом поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, busy_place):
        """Метод генерирующий новую позицию объекта на поле."""
        while True:
            new_position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                            randrange(0, SCREEN_HEIGHT, GRID_SIZE))
            if new_position in busy_place:
                continue
            else:
                self.position = new_position
                break


class Snake(GameObject):
    """Класс описываюющий саму змею."""

    def __init__(self, color=None):
        """Конструктор класса.

        В нём задаётся список состоящий из кортежей.
        Цвет змейки.
        """
        super().__init__(color)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.body_color = color
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
        x, y = self.get_head_position()
        direction_x, direction_y = self.direction
        head = (x + (GRID_SIZE * direction_x),
                y + (direction_y * GRID_SIZE))
        self.positions.insert(0, head)
        self.last = self.positions[-1]

    def check_to_reset(self):
        """Метод проверяющий врезалась ли змейка сама в себя."""
        if self.get_head_position() in self.positions[2:]:
            return True

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

    def out_of_boards(self):
        """Метод позволяющий змейке переходить через стены."""
        x, y = self.get_head_position()
        if x > SCREEN_WIDTH:
            self.positions[0] = (START_BOARD, y)
        elif x < 0:
            self.positions[0] = (SCREEN_WIDTH, y)
        elif y > SCREEN_HEIGHT:
            self.positions[0] = (x, START_BOARD)
        elif y < 0:
            self.positions[0] = (x, SCREEN_HEIGHT)

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
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.positions[0] == apple.position:
            apple.randomize_position(snake.positions)
            snake.length += 1
        else:
            snake.positions.pop()
        snake.out_of_boards()
        if snake.check_to_reset():
            snake.reset()
            apple.position = CENTER_OF_BOARD
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
