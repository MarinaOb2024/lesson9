import pygame
import random
import sys
import time

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра на выживание")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Параметры игрока
player_size = 50
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5

# Параметры врага
enemy_size = 50
enemy_speed = 3
enemies = []


# Функция для создания нового врага
def spawn_enemy():
    x_pos = random.randint(0, WIDTH - enemy_size)
    y_pos = random.randint(0, HEIGHT - enemy_size)
    enemies.append([x_pos, y_pos])


# Функция для передвижения врагов к игроку
def move_enemies():
    for enemy in enemies:
        if enemy[0] < player_pos[0]:
            enemy[0] += enemy_speed
        elif enemy[0] > player_pos[0]:
            enemy[0] -= enemy_speed

        if enemy[1] < player_pos[1]:
            enemy[1] += enemy_speed
        elif enemy[1] > player_pos[1]:
            enemy[1] -= enemy_speed


# Проверка на столкновение
def check_collision(player_pos, enemy_pos):
    p_x, p_y = player_pos
    e_x, e_y = enemy_pos
    return (e_x < p_x < e_x + enemy_size or e_x < p_x + player_size < e_x + enemy_size) and \
        (e_y < p_y < e_y + enemy_size or e_y < p_y + player_size < e_y + enemy_size)


# Основной игровой цикл
clock = pygame.time.Clock()
start_time = time.time()

running = True
while running:
    screen.fill(WHITE)

    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_s] and player_pos[1] < HEIGHT - player_size:
        player_pos[1] += player_speed
    if keys[pygame.K_a] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_d] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed

    # Добавление врагов со временем
    if random.randint(0, 100) < 3:
        spawn_enemy()

    # Движение врагов
    move_enemies()

    # Проверка на столкновение с каждым врагом
    for enemy in enemies:
        if check_collision(player_pos, enemy):
            running = False

    # Отрисовка игрока
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    # Отрисовка врагов
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_size, enemy_size))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(30)

# Конец игры
screen.fill(WHITE)
end_time = time.time() - start_time
font = pygame.font.SysFont("Arial", 40)
text = font.render(f"Вы продержались: {int(end_time)} секунд", True, RED)
screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
pygame.display.flip()

# Ожидание перед закрытием
pygame.time.delay(3000)
pygame.quit()
sys.exit()
