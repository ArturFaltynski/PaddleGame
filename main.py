import pygame
import sys
def draw_player(screen, player_rect, color=(255, 255, 255)):
    pygame.draw.rect(screen, color, player_rect)

def draw_ball(screen, ball_rect, color=(255, 0, 0)):
    pygame.draw.ellipse(screen, color, ball_rect)
def reset_ball(ball_rect):
    ball_rect.x = screen_width // 2 - ball_width // 2
    ball_rect.y = screen_height // 2 - ball_height // 2
def reset_game():
    global score_player1, score_player2, running, game_over
    score_player1 = 0
    score_player2 = 0
    running = True
    game_over = False
    reset_ball(ball_rect)
def display_winner(screen, winner):
    font = pygame.font.Font(None, 74)
    win_text = font.render(f"{winner} Wins!", True, (255, 255, 255))
    screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - win_text.get_height() // 2 - 30))

    # Przycisk restartu
    restart_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 10, 200, 40)
    pygame.draw.rect(screen, (0, 255, 0), restart_button)
    restart_text = font.render("Restart", True, (255, 255, 255))
    screen.blit(restart_text, (restart_button.x + (200 - restart_text.get_width()) // 2, restart_button.y + 5))
    return restart_button
# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Ustawienia gracza 1
player_width = 200
player_height = 10
player1_x = screen_width // 2 - player_width // 2
player1_y = screen_height - player_height - 30
player_speed = 5
player1_rect = pygame.Rect(player1_x, player1_y, player_width, player_height)

# Ustawienia gracza 2
player2_x = screen_width // 2 - player_width // 2
player2_y = 30
player2_rect = pygame.Rect(player2_x, player2_y, player_width, player_height)

# Ustawienia piłki
ball_width = 15
ball_height = 15
ball_x = screen_width // 2 - ball_width // 2
ball_y = screen_height // 2 - ball_height // 2
ball_speed_x = 5
ball_speed_y = 5
ball_rect = pygame.Rect(ball_x, ball_y, ball_width, ball_height)

# Wyniki graczy
score_player1 = 0
score_player2 = 0

# Kolor tła
background_color = (0, 0, 0)  # Czarny
# Inicjalizacja zegara Pygame
clock = pygame.time.Clock()
fps = 45  # Ustawienie liczby klatek na sekundę na 25

# Pętla gry
# Stan gry
running = True
game_over = False
restart_button = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_over and event.type == pygame.MOUSEBUTTONDOWN and restart_button.collidepoint(event.pos):
            reset_game()
    if running:

        # Sterowanie graczem 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player1_rect.x -= player_speed
        if keys[pygame.K_d]:
            player1_rect.x += player_speed

        # Sterowanie graczem 2
        if keys[pygame.K_LEFT]:
            player2_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player2_rect.x += player_speed

        # Zapobieganie wyjściu poza ekran dla obu graczy
        player1_rect.x = max(player1_rect.x, 0)
        player1_rect.x = min(player1_rect.x, screen_width - player_width)
        player2_rect.x = max(player2_rect.x, 0)
        player2_rect.x = min(player2_rect.x, screen_width - player_width)

        # Ruch piłki
        ball_rect.x += ball_speed_x
        ball_rect.y += ball_speed_y

        # Odbicie od ścian
        if ball_rect.left <= 0 or ball_rect.right >= screen_width:
            ball_speed_x *= -1
        if ball_rect.top <= 0 or ball_rect.bottom >= screen_height:
            ball_speed_y *= -1

        # Kolizja z graczami
        if ball_rect.colliderect(player1_rect) or ball_rect.colliderect(player2_rect):
            ball_speed_y *= -1

         # Logika punktacji
        if ball_rect.top <= 0:
            score_player1 += 1
            reset_ball(ball_rect)
        elif ball_rect.bottom >= screen_height:
            score_player2 += 1
            reset_ball(ball_rect)
        # Sprawdzenie, czy gracz zdobył 5 punktów
        if score_player1 >= 5:
            display_winner(screen, "Player 1")
            game_over = True
            running = False
        elif score_player2 >= 5:
            display_winner(screen, "Player 2")
            game_over = True
            running = False

        # Wypełnienie tła
        screen.fill(background_color)

        # Wyświetlanie wyników (opcjonalnie)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"P1: {score_player1}  P2: {score_player2}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        # Rysowanie graczy i piłki
        draw_player(screen, player1_rect)
        draw_player(screen, player2_rect, color=(0, 255, 0))
        draw_ball(screen, ball_rect)



    else:
        # Gra zakończona, wyświetlenie przycisku restartu
        if game_over:
            restart_button = display_winner(screen, "Player 1" if score_player1 >= 5 else "Player 2")
            # Odświeżenie ekranu
    pygame.display.flip()
    clock.tick(fps)


# Zamykanie Pygame
pygame.quit()
