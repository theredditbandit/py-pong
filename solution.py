import pygame

pygame.init()

WIDTH, HEIGHT = 700, 500  # declaring width and height as variables so that our window can be dynamic
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # this is for the window
pygame.display.set_caption("Pong")  # caption
FPS = 60  # storing consstant variables as capital names
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans", 50)


class Paddle:
    COLOUR = WHITE
    VEL = 4  # velocity with which the paddles will move

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOUR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):  # method to move the paddle up or down.
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


def draw(win, paddles, ball, left_score, right_score):  # this function draws everything that we see on the screen
    win.fill(BLACK)
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))
    for paddle in paddles:
        paddle.draw(win)

    # this for loop below draws the centre dotted white line on the board.
    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))
    ball.draw(win)

    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    if ball.x_vel < 0:  # checking collision with the left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:  # right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
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


def main():  # event / game loop
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        handle_collision(ball, left_paddle, right_paddle)
        handle_paddle_movement(keys, left_paddle, right_paddle)
        if ball.x + ball.radius >= WIDTH:
            left_score += 1
            ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
            ball.x_vel *= -1
        elif ball.x - ball.radius <= 0:
            right_score += 1
            ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
            ball.x_vel *= -1
        ball.move()
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)
    pygame.quit()


main()
