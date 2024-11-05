"""Импортируемые библиотеки."""
from random import choice, randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

all_dicretion = [UP, DOWN, LEFT, RIGHT]

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

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс для создания игровых объектов."""

    def __init__(self):
        """Конструктор класса.

        С заданными по умолчанию позицией объекта и его цветом.
        """
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color = None


class Apple(GameObject):
    """Класс описывающий яблоко на игровом поле."""

    def __init__(self):
        """Конструктор класса, где задана позиция и поменян цвет объекта."""
        super().__init__()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Метод отрисовывающий объект на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Метод генерирующий новую позицию объекта на поле."""
        self.new_position = randrange(0, 640, 20), randrange(0, 480, 20)
        self.position = self.new_position


apple = Apple()


class Snake(GameObject):
    """Класс описываюющий саму змею.

    Имеет начальное направление, начальную длину.
    """

    length = 1
    direction = RIGHT
    next_direction = None
    positions: list = []

    def __init__(self):
        """Конструктор класса.

        В нём задаётся список состоящий из кортежей.
        Цвет змейки.
        """
        super().__init__()
        self.positions.insert(0, self.position)
        self.body_color = SNAKE_COLOR
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
        head = (x + (GRID_SIZE * self.direction[0]),
                y + (self.direction[1] * GRID_SIZE))
        self.positions.insert(0, head)
        self.last = self.positions[-1]

    def check_eat_apple(self):
        """Метод проверяющий съела ли змейка яблоко."""
        if self.positions[0] == apple.position:
            self.length += 1
            apple.randomize_position()
            apple.draw()
        else:
            self.positions.pop()

    def check_to_reset(self):
        """Метод проверяющий врезалась ли змейка сама в себя."""
        if self.positions[0] in self.positions[3:] and self.length > 3:
            self.reset()

    def draw(self):
        """Метод отрисовывающий змейку."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def out_of_boards(self):
        """Метод позволяющий змейке переходить через стены."""
        if self.positions[0][0] > SCREEN_WIDTH:
            self.positions[0] = (0, self.positions[0][1])
        elif self.positions[0][0] < 0:
            self.positions[0] = (640, self.positions[0][1])
        elif self.positions[0][1] > SCREEN_HEIGHT:
            self.positions[0] = (self.positions[0][0], 0)
        elif self.positions[0][1] < 0:
            self.positions[0] = (self.positions[0][0], 480)

    def reset(self):
        """Метод прерывающий игру."""
        self.positions = [self.position]
        apple.position = self.position
        self.length = 1
        self.direction = choice(all_dicretion)
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция main, в ней запускается вся игра."""
    pygame.init()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.check_eat_apple()
        snake.check_to_reset()
        snake.out_of_boards()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
