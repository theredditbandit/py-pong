from turtle import left, width
import pygame 
pygame.init()

WIDTH,HEIGHT = 700,500 # declaring width and height as variables so that our window can be dynamic
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) # this is for the window
pygame.display.set_caption("Pong") # caption 
FPS = 60 # storing consstant variables as capital names
WHITE = (255,255,255)
BLACK = (0,0,0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20,100

class Paddle:
    COLOUR = WHITE
    VEL = 4 # velocity with which the paddles will move 
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def draw(self,win):
        pygame.draw.rect(win,self.COLOUR,(self.x,self.y,self.width,self.height))
    def move(self,up=True): # method to move the paddle up or down. 
        if up:
            self.y -=self.VEL
        else:
            self.y += self.VEL


def draw(win,paddles): # this function draws everything that we see on the screen 
    win.fill(BLACK)
    for paddle in paddles:
        paddle.draw(win)
    
    # this for loop below draws the centre dotted white line on the board. 
    for i in range(10,HEIGHT,HEIGHT//20):
        if i%2 == 1:
            continue
        pygame.draw.rect(win,WHITE,(WIDTH//2-5,i,10,HEIGHT//20))

    
    pygame.display.update()

def handle_paddle_movement(keys,left_paddle,right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >=0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <=HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >=0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <=HEIGHT:
        right_paddle.move(up=False)

def main(): # event / game loop 
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)

    while run: 
        clock.tick(FPS) # regulates the speed of the while loop
        draw(WIN,[left_paddle,right_paddle])
        for event in pygame.event.get(): # this will get all the events that occour
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys,left_paddle,right_paddle)
    pygame.quit()

if __name__ == '__main__':
    main()


