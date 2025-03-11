import pygame
import sys

pygame.init()
W, H = 800, 600
FPS = 60
BS = 5
SPEED = 7
WC = (255, 255, 255)
BC = (0, 0, 0)
root = pygame.display.set_mode((W, H))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()
ball = pygame.Rect(W // 2 - 15, H // 2 - 15, 30, 30)
bx, by = BS, BS
player1 = pygame.Rect(20, H // 2 - 60, 10, 120)
player2 = pygame.Rect(W - 30, H // 2 - 60, 10, 120)
p1 = 0
p2 = 0
font = pygame.font.Font(None, 74)
game_mode = "single"
player1_color = WC
player2_color = WC
hit_sound = pygame.mixer.Sound("hit.wav")
score_sound = pygame.mixer.Sound("score.wav")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

def select_game_mode():
    global game_mode
    selected = False
    while not selected:
        root.fill(BC)
        title = font.render("Select Game Mode", True, WC)
        mode1 = font.render("1 - Single Player (vs AI)", True, WC)
        mode2 = font.render("2 - Two Players", True, WC)
        root.blit(title, (W//2 - title.get_width()//2, H//2 - 100))
        root.blit(mode1, (W//2 - mode1.get_width()//2, H//2 - 25))
        root.blit(mode2, (W//2 - mode2.get_width()//2, H//2 + 50))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_mode = "single"
                    selected = True
                elif event.key == pygame.K_2:
                    game_mode = "two_players"
                    selected = True

def select_colors():
    global player1_color, player2_color
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255)
    ]
    current_player = 1
    color_index = 0
    while current_player <= 2:
        root.fill(BC)
        title = font.render(f"Player {current_player} Color", True, WC)
        root.blit(title, (W//2 - title.get_width()//2, 50))
        for i, color in enumerate(colors):
            pygame.draw.rect(root, color, (W//2 - 150 + i*60, H//2 - 30, 50, 50))
        pygame.draw.rect(root, WC, (W//2 - 153 + color_index*60, H//2 - 33, 56, 56), 3)
        inst = font.render("Use ← → to choose, ENTER to confirm", True, WC)
        root.blit(inst, (W//2 - inst.get_width()//2, H - 100))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    color_index = (color_index - 1) % len(colors)
                elif event.key == pygame.K_RIGHT:
                    color_index = (color_index + 1) % len(colors)
                elif event.key == pygame.K_RETURN:
                    if current_player == 1:
                        player1_color = colors[color_index]
                        current_player = 2
                        color_index = 0
                    else:
                        player2_color = colors[color_index]
                        current_player = 3

def drawobjects():
    root.fill(BC)
    pygame.draw.rect(root, player1_color, player1)
    pygame.draw.rect(root, player2_color, player2)
    pygame.draw.ellipse(root, WC, ball)
    pygame.draw.aaline(root, WC, (W // 2, 0), (W // 2, H))
    score_text = font.render(f"{p1}  {p2}", True, WC)
    root.blit(score_text, (W // 2 - score_text.get_width()//2, 20))

def mvball():
    global bx, by, p1, p2, SPEED
    ball.x += bx
    ball.y += by
    if ball.top <= 0 or ball.bottom >= H:
        by = -by
    if ball.left <= 0:
        p2 += 1
        score_sound.play()
        rsball()
    if ball.right >= W:
        p1 += 1
        score_sound.play()
        rsball()
    if ball.colliderect(player1) or ball.colliderect(player2):
        bx = -bx
        hit_sound.play()

def rsball():
    global bx, by
    ball.center = (W // 2, H // 2)
    bx = -bx
    if abs(bx) < 15:
        bx *= 1.1
        by *= 1.1

def mvpads():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= SPEED
    if keys[pygame.K_s] and player1.bottom < H:
        player1.y += SPEED
    if game_mode == "two_players":
        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= SPEED
        if keys[pygame.K_DOWN] and player2.bottom < H:
            player2.y += SPEED
    else:
        if player2.centery < ball.centery:
            player2.y += SPEED
        elif player2.centery > ball.centery:
            player2.y -= SPEED
        if player2.top < 0:
            player2.top = 0
        if player2.bottom > H:
            player2.bottom = H

def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
        pause_text = font.render("Paused", True, WC)
        root.blit(pause_text, (W//2 - pause_text.get_width()//2, H//2 - pause_text.get_height()//2))
        pygame.display.update()

def main():
    global p1, p2
    select_game_mode()
    select_colors()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_game()
        mvpads()
        mvball()
        drawobjects()
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
