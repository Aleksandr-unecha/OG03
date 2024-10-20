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
target_radius = 60
target_x = random.randint(target_radius, SCREEN_WIDTH - target_radius)
target_y = random.randint(target_radius, SCREEN_HEIGHT - target_radius)

# Скорость мишени
target_speed_x = random.choice([-1, 1])
target_speed_y = random.choice([-1, 1])

# Скрыть стандартный курсор мыши
pygame.mouse.set_visible(False)

# Шрифт для отображения очков
font = pygame.font.Font(None, 36)
target_font = pygame.font.Font(None, 24)  # Шрифт для цифр в мишени
score = 0


def calculate_score(mouse_x, mouse_y, target_x, target_y):
    """Функция для вычисления очков на основе положения клика"""
    distance = math.hypot(target_x - mouse_x, target_y - mouse_y)
    if distance <= target_radius:
        return 10 - int(distance // 10) * 2
    return 0


def draw_target(x, y):
    """Функция для рисования мишени с цифрами и полосами"""
    # Цвета: черный, белый
    colors = [(0, 0, 0), (255, 255, 255)]
    target_data = [
        (0, 50, '1'),  # Внешний черный круг
        (1, 40, '2'),  # Белый круг
        (0, 30, '3'),  # Черный круг
        (1, 20, '4'),  # Белый круг
        (0, 10, None)  # Черная центральная точка без цифры
    ]

    for color_index, radius, text in target_data:
        color = colors[color_index]
        pygame.draw.circle(screen, color, (x, y), radius)
        if text and text != '10':
            # Цвет текста белый (255, 255, 255)
            text_surf = target_font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(x, y))
            screen.blit(text_surf, text_rect)

    # Черные полосы по осям X и Y
    line_color = (0, 0, 0)
    line_width = 3
    pygame.draw.line(screen, line_color, (x - target_radius, y), (x + target_radius, y), line_width)
    pygame.draw.line(screen, line_color, (x, y - target_radius), (x, y + target_radius), line_width)

    # Отрисовка цифры "10" поверх всех слоев
    text_surf = target_font.render('10', True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x, y))
    screen.blit(text_surf, text_rect)

clock = pygame.time.Clock()
running = True
while running:
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            gunshot_sound.play()

            mouse_x, mouse_y = pygame.mouse.get_pos()
            points = calculate_score(mouse_x, mouse_y, target_x, target_y)
            if points > 0:
                score += points
                target_x = random.randint(target_radius, SCREEN_WIDTH - target_radius)
                target_y = random.randint(target_radius, SCREEN_HEIGHT - target_radius)

    # Обновление позиции мишени
    target_x += target_speed_x
    target_y += target_speed_y

    # Обработка границ экрана
    if target_x <= target_radius or target_x >= SCREEN_WIDTH - target_radius:
        target_speed_x *= -1
    if target_y <= target_radius or target_y >= SCREEN_HEIGHT - target_radius:
        target_speed_y *= -1

    draw_target(target_x, target_y)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(crosshair_img, (mouse_x - crosshair_img.get_width() // 2, mouse_y - crosshair_img.get_height() // 2))

    score_text = font.render(f"Очки: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()