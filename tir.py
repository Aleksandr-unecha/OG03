import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра Тир")

# Загрузка изображений
try:
    background_img = pygame.image.load("img/background.jpg")
    crosshair_img = pygame.image.load("img/crosshair.png")
    target_img = pygame.image.load("img/target.png")  # Новое изображение мишени
    icon = pygame.image.load("img/55100.jpg")
    pygame.display.set_icon(icon)
except pygame.error as e:
    print(f"Ошибка загрузки изображений: {e}")
    pygame.quit()
    exit()

# Загрузка звука выстрела
try:
    gunshot_sound = pygame.mixer.Sound("img/gunshot.wav")
except pygame.error as e:
    print(f"Ошибка загрузки звука: {e}")
    pygame.quit()
    exit()

# Параметры мишени
target_rect = target_img.get_rect()
target_radius = target_rect.width // 2  # Предполагаем, что изображение круглое
target_x = random.randint(target_radius, SCREEN_WIDTH - target_radius)
target_y = random.randint(target_radius, SCREEN_HEIGHT - target_radius)

# Скорость мишени
target_speed_x = random.choice([-1, 1])
target_speed_y = random.choice([-1, 1])

# Скрыть стандартный курсор мыши
pygame.mouse.set_visible(False)

# Шрифт для отображения очков
font = pygame.font.Font(None, 36)

score = 0

def calculate_score(mouse_x, mouse_y, target_x, target_y):
    """Функция для вычисления очков на основе положения клика"""
    distance = math.hypot(target_x - mouse_x, target_y - mouse_y)
    if distance <= target_radius:
        return 10 - int(distance // 10) * 2
    return 0

def draw_target(x, y):
    """Функция для рисования мишени"""
    # Отрисовка мишени
    target_rect.center = (x, y)
    screen.blit(target_img, target_rect)

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if calculate_score(mouse_x, mouse_y, target_x, target_y) > 0:
                score += calculate_score(mouse_x, mouse_y, target_x, target_y)
                gunshot_sound.play()
# Обновление позиции цели
    target_x += target_speed_x
    target_y += target_speed_y

    # Проверка границ экрана
    if target_x - target_radius < 0 or target_x + target_radius > SCREEN_WIDTH:
        target_speed_x *= -1
    if target_y - target_radius < 0 or target_y + target_radius > SCREEN_HEIGHT:
        target_speed_y *= -1

    # Отрисовка фона и мишени
    screen.blit(background_img, (0, 0))
    draw_target(target_x, target_y)

    # Отрисовка перекрестия
    crosshair_rect = crosshair_img.get_rect(center=pygame.mouse.get_pos())
    screen.blit(crosshair_img, crosshair_rect)

    # Обновление экрана
    pygame.display.flip()

pygame.quit()