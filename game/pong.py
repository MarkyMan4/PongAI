import pygame
import sys
from joblib import load
from random import random

# load the model for the AI player
model = load('model.joblib')

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100

# position of player paddle
PLAYER_X = 50
player_y = (SCREEN_HEIGHT / 2) - (PADDLE_HEIGHT / 2)

# position of the AI's paddle
AI_X = SCREEN_WIDTH - 100
ai_y = (SCREEN_HEIGHT / 2) - (PADDLE_HEIGHT / 2)

# prediction_history = []

BALL_RADIUS = 10
ball_x = SCREEN_WIDTH / 2
ball_y = SCREEN_HEIGHT / 2
ball_x_vel = -0.5
ball_y_vel = -0.25

game_over = False

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill((20,20,20))
pygame.display.set_caption('Pong')

def update_player_and_ball():
    # draw the player's paddle
    pygame.draw.rect(
        screen, 
        (255,255,255), 
        (PLAYER_X, player_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    )

    # draw the AI's paddle
    pygame.draw.rect(
        screen, 
        (255,255,255), 
        (AI_X, ai_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    )

    # draw the ball
    pygame.draw.circle(
        screen,
        (255,255,255),
        (ball_x, ball_y),
        BALL_RADIUS
    )

def update_ai_pos():
    global ball_x
    global ball_y
    global ball_x_vel
    global ball_y_vel
    global ai_y
    # global prediction_history

    prediction = model.predict([[ball_x, ball_y, ball_x_vel, ball_y_vel]])[0][0]

    # if len(prediction_history) >= 75:
    #     prediction_history.pop()

    # if the predicted paddle position is less than the current position move up by 1
    # if it's greater than the current position, move down by 1, otherwise stay in place
    if prediction < ai_y:
        ai_y -= 1
        # prediction_history = ['up'] + prediction_history
    elif prediction > ai_y:
        ai_y += 1
        # prediction_history = ['down'] + prediction_history

    # up_count = 0
    # down_count = 0

    # for p in prediction_history:
    #     if p == 'up':
    #         up_count += 1
    #     else:
    #         down_count += 1

    # if up_count >= down_count:
    #     ai_y -= 1
    # else:
    #     ai_y += 1

def update_ball_pos():
    global ball_x
    global ball_y
    global ball_x_vel
    global ball_y_vel
    global game_over

    ball_x += ball_x_vel
    ball_y += ball_y_vel

    # check if ball collided with the right wall
    # if ball_x >= SCREEN_WIDTH:
    #     ball_x_vel *= -1
    
    # check if ball collided with top or bottom wall
    if ball_y <= 0 or ball_y >= SCREEN_HEIGHT:
        ball_y_vel *= -1

    # check if ball collided with a paddle
    if (ball_x <= PLAYER_X + PADDLE_WIDTH and ball_y >= player_y and ball_y <= player_y + PADDLE_HEIGHT) \
            or (ball_x >= AI_X and ball_y >= ai_y and ball_y <= ai_y + PADDLE_HEIGHT):
        ball_x_vel *= -1

    # check if ball went off the screen
    if ball_x <= 0 or ball_x >= SCREEN_WIDTH:
        game_over = True


def main_loop():
    """
    main loop for the game

    The commented out lines are used for recording ball and player positions
    that are used to train the AI model to play the game.
    """
    global game_over
    global player_y
    global ball_x_vel
    global ball_y_vel

    # start the ball in a random direction
    if int(random() * 2) == 1:
        ball_x_vel *= -1

    if int(random() * 2) == 1:
        ball_y_vel *= -1

    # this file stores the info about the ball and players position
    # positions = open('positions2.csv', 'w')
    # positions.write('ball_x,ball_y,ball_x_vel,ball_y_vel,player_y\n')

    while not game_over:
        # positions.write(f'{ball_x},{ball_y},{ball_x_vel},{ball_y_vel},{player_y}\n')

        screen.fill((20,20,20))
        update_player_and_ball()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            player_y -= 1
        elif keys[pygame.K_s]:
            player_y += 1
        elif keys[pygame.K_ESCAPE]: # escape to quite the game
            game_over = True

        update_ai_pos()
        update_ball_pos()

        pygame.display.update()

    # positions.close()

if __name__ == '__main__':
    main_loop()
    pygame.quit()
    quit()