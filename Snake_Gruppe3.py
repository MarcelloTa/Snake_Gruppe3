def eat_apple():
    global apple_pos, score, snake_body

    if abs(snake_pos[0] - apple_pos[0]) < snake_size and abs(snake_pos[1] - apple_pos[1]) < snake_size:
        # Neue Platzierung des Apfels
        while True:
            new_apple_pos = [random.randint(0, (screen_width // apple_size) - 1) * apple_size,
                             random.randint(0, (screen_height // apple_size) - 1) * apple_size]
            if new_apple_pos not in snake_body:
                apple_pos[0] = new_apple_pos[0]
                apple_pos[1] = new_apple_pos[1]
                break
        score += 10
        snake_body.append(snake_body[-1])  # Die Schlange wächst

# Hauptspielschleife
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

    move_snake()
    eat_apple()

    screen.fill(BLACK)

    pygame.draw.rect(screen, RED, pygame.Rect(apple_pos[0], apple_pos[1], apple_size, apple_size))
    
    for pos in snake_body:
        pygame.draw.rect(screen, snake_color, pygame.Rect(pos[0], pos[1], snake_size, snake_size))

    score_surface = font.render(f'Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (screen_width / 2, 10)
    screen.blit(score_surface, score_rect)

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
