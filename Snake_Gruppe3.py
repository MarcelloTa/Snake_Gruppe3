import pygame
import random
import sys
#Dorians push und fetch
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Einfaches Snake-Spiel')

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (192, 192, 192)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
COLORS = [GREEN, BLUE, RED, GRAY, WHITE]

snake_size = 20
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction
snake_color = GREEN

apple_size = 20
apple_pos = [random.randint(0, (screen_width // apple_size) - 1) * apple_size,
             random.randint(0, (screen_height // apple_size) - 1) * apple_size]

walls_level_2 = [
    pygame.Rect(200, 200, 20, 200),
    pygame.Rect(400, 200, 20, 200)
]

speed = 15
clock = pygame.time.Clock()

score = 0
level = 1

smoke_particles = []

enemy_snakes = [
    {'body': [[600, 50], [590, 50], [580, 50]], 'direction': 'LEFT', 'color': BLUE},
    {'body': [[600, 150], [590, 150], [580, 150]], 'direction': 'LEFT', 'color': RED}
]

def game_over():
    font = pygame.font.SysFont('times new roman', 50)
    go_surface = font.render(f'Game Over! Score: {score}', True, RED)
    go_rect = go_surface.get_rect()
    go_rect.midtop = (screen_width / 2, screen_height / 4)
    screen.blit(go_surface, go_rect)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def create_smoke(pos):
    smoke_particles.append({'pos': pos[:], 'radius': 10, 'lifespan': 20})

def update_smoke():
    for particle in smoke_particles[:]:
        particle['pos'][1] -= 1
        particle['radius'] -= 0.5
        particle['lifespan'] -= 1
        if particle['lifespan'] <= 0:
            smoke_particles.remove(particle)

def draw_walls(walls):
    for wall in walls:
        pygame.draw.rect(screen, BLUE, wall)

def change_snake_color():
    global snake_color
    snake_color = random.choice(COLORS)

def move_enemy_snakes():
    for enemy_snake in enemy_snakes:
        if abs(enemy_snake['body'][0][0] - snake_pos[0]) > abs(enemy_snake['body'][0][1] - snake_pos[1]):
            if enemy_snake['body'][0][0] < snake_pos[0]:
                enemy_snake['direction'] = 'RIGHT'
            else:
                enemy_snake['direction'] = 'LEFT'
        else:
            if enemy_snake['body'][0][1] < snake_pos[1]:
                enemy_snake['direction'] = 'DOWN'
            else:
                enemy_snake['direction'] = 'UP'

        if enemy_snake['direction'] == 'LEFT':
            enemy_snake['body'][0][0] -= snake_size
        elif enemy_snake['direction'] == 'RIGHT':
            enemy_snake['body'][0][0] += snake_size
        elif enemy_snake['direction'] == 'UP':
            enemy_snake['body'][0][1] -= snake_size
        elif enemy_snake['direction'] == 'DOWN':
            enemy_snake['body'][0][1] += snake_size

        enemy_snake['body'].insert(0, list(enemy_snake['body'][0]))
        enemy_snake['body'].pop()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    direction = change_to

    if direction == 'UP':
        snake_pos[1] -= snake_size
    if direction == 'DOWN':
        snake_pos[1] += snake_size
    if direction == 'LEFT':
        snake_pos[0] -= snake_size
    if direction == 'RIGHT':
        snake_pos[0] += snake_size

    snake_body.insert(0, list(snake_pos))

    if abs(snake_pos[0] - apple_pos[0]) < snake_size and abs(snake_pos[1] - apple_pos[1]) < snake_size:
        create_smoke(list(snake_pos))
        apple_pos = [random.randint(0, (screen_width // apple_size) - 1) * apple_size,
                     random.randint(0, (screen_height // apple_size) - 1) * apple_size]
        score += 10
        change_snake_color()
    else:
        snake_body.pop()

    if snake_pos[0] < 0:
        snake_pos[0] = screen_width - snake_size
    elif snake_pos[0] >= screen_width:
        snake_pos[0] = 0
    elif snake_pos[1] < 0:
        snake_pos[1] = screen_height - snake_size
    elif snake_pos[1] >= screen_height:
        snake_pos[1] = 0

    if score >= 100:
        level = 2

    screen.fill(BLACK)

    update_smoke()

    pygame.draw.rect(screen, RED, pygame.Rect(apple_pos[0], apple_pos[1], apple_size, apple_size))

    for particle in smoke_particles:
        pygame.draw.circle(screen, GRAY, particle['pos'], int(particle['radius']))

    for pos in snake_body:
        pygame.draw.rect(screen, snake_color, pygame.Rect(pos[0], pos[1], snake_size, snake_size))

    if level == 2:
        draw_walls(walls_level_2)
        for wall in walls_level_2:
            if wall.collidepoint(snake_pos):
                game_over()

    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    if level == 2:
        move_enemy_snakes()
        for enemy_snake in enemy_snakes:
            for pos in enemy_snake['body']:
                pygame.draw.rect(screen, enemy_snake['color'], pygame.Rect(pos[0], pos[1], snake_size, snake_size))
            if abs(snake_pos[0] - enemy_snake['body'][0][0]) < snake_size and abs(snake_pos[1] - enemy_snake['body'][0][1]) < snake_size:
                game_over()

    font = pygame.font.SysFont('times new roman', 20)
    score_surface = font.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (screen_width / 2, 10)
    screen.blit(score_surface, score_rect)

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
#Birol