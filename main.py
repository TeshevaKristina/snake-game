import random
import pygame

# Размеры игрового окна.
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
# Размер одной ячейки сетки.
GRID_SIZE = 20
# Количество кадров в секунду.
FPS = 20

# Цвета.
BOARD_BACKGROUND_COLOR = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        """Инициализирует базовые атрибуты объекта."""
        # Позиция по умолчанию — центр экрана.
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self, surface):
        """Метод для отрисовки объекта, переопределяется в наследниках."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Задает цвет яблока и устанавливает начальную позицию."""
        super().__init__()
        self.body_color = RED
        # Сразу задаем случайную позицию при создании яблока.
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        max_x = SCREEN_WIDTH // GRID_SIZE - 1
        max_y = SCREEN_HEIGHT // GRID_SIZE - 1
        self.position = (
            random.randint(0, max_x) * GRID_SIZE,
            random.randint(0, max_y) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = (GRID_SIZE, 0)  # По умолчанию движется вправо.
        self.next_direction = None
        self.body_color = GREEN
        # Атрибут для хранения позиции удаленного хвоста.
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            # Запрещаем разворот на 180 градусов.
            if (self.next_direction[0] != -self.direction[0] or
                    self.next_direction[1] != -self.direction[1]):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        # Вычисляем новые координаты головы.
        new_head = (head_x + dx, head_y + dy)

        # Обработка прохода сквозь границы экрана.
        new_head = (
            new_head[0] % SCREEN_WIDTH,
            new_head[1] % SCREEN_HEIGHT
        )

        # Добавляем новую голову.
        self.positions.insert(0, new_head)

        # Если змейка не выросла, запоминаем хвост и удаляем его.
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        # Затираем след от предыдущего хвоста.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        # Случайное направление при перезапуске.
        directions = [(0, -GRID_SIZE), (0, GRID_SIZE), 
                      (-GRID_SIZE, 0), (GRID_SIZE, 0)]
        self.direction = random.choice(directions)
        self.next_direction = None
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != (0, GRID_SIZE):
                snake.next_direction = (0, -GRID_SIZE)
            elif event.key == pygame.K_DOWN and snake.direction != (0, -GRID_SIZE):
                snake.next_direction = (0, GRID_SIZE)
            elif event.key == pygame.K_LEFT and snake.direction != (GRID_SIZE, 0):
                snake.next_direction = (-GRID_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake.direction != (-GRID_SIZE, 0):
                snake.next_direction = (GRID_SIZE, 0)


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Если змейка съела яблоко.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка столкновения с самой собой.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            # Очищаем экран после рестарта.
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()