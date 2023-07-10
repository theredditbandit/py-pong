import pygame
import random

pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)   
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans", 50)


class Paddle:
    COLOUR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOUR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL


class Ball:
    MAX_VEL = 5
    COLOUR = WHITE

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOUR, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)
    left_score_text = SCORE_FONT.render(str(left_score), 1, WHITE)
    right_score_text = SCORE_FONT.render(str(right_score), 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))
    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))
    ball.draw(win)

    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0 and ball.x - ball.radius <= left_paddle.x + left_paddle.width:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            ball.x_vel *= -1
            middle_y = left_paddle.y + left_paddle.height / 2
            difference_in_y = middle_y - ball.y
            reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
            y_vel = difference_in_y / reduction_factor
            ball.y_vel = -1 * y_vel

    elif ball.x_vel > 0 and ball.x + ball.radius >= right_paddle.x:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            ball.x_vel *= -1
            middle_y = right_paddle.y + right_paddle.height / 2
            difference_in_y = middle_y - ball.y
            reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
            y_vel = difference_in_y / reduction_factor
            ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


def show_game_over_screen(winner):
    font = pygame.font.SysFont("comicsans", 60)
    text = font.render(f"Game Over - {winner} wins!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        WIN.fill(BLACK)
        WIN.blit(text, text_rect)
        pygame.display.update()


def main(play_against_bot, max_score):
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    left_score = 0
    right_score = 0

    game_over = False
    winner = None

    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not game_over:
            handle_collision(ball, left_paddle, right_paddle)
            handle_paddle_movement(keys, left_paddle, right_paddle)

            if play_against_bot:
                # Bot logic goes here
                if ball.y < right_paddle.y + right_paddle.height / 2:
                    if right_paddle.y - right_paddle.VEL >= 0:
                        right_paddle.move(up=True)
                else:
                    if right_paddle.y + right_paddle.height + right_paddle.VEL <= HEIGHT:
                        right_paddle.move(up=False)

            if ball.x + ball.radius >= WIDTH:
                left_score += 1
                if left_score >= max_score:
                    game_over = True
                    winner = "Player 1"
                else:
                    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
                    ball.x_vel *= random.choice([1, -1])

            elif ball.x - ball.radius <= 0:
                right_score += 1
                if right_score >= max_score:
                    game_over = True
                    winner = "Player 2"
                else:
                    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
                    ball.x_vel *= random.choice([1, -1])

            ball.move()
            draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        else:
            show_game_over_screen(winner)

    pygame.quit()



if __name__ == "__main__":
    play_against_bot = input("Do you want to play against a bot? (yes/no): ").lower() == "yes"
    max_score = int(input("Enter the maximum score: "))
    main(play_against_bot, max_score)


main()

