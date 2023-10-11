#```python Simple Snake Game

import pygame
import time
import random
import sys

# Initialize the pygame, Title and icon
pygame.init()
pygame.display.set_caption('SNAKE GAME')
icon = pygame.image.load("icon/snake.jpeg")
pygame.display.set_icon(icon)


import logging
logging.basicConfig(level=logging.DEBUG, filename="Handler.log", format='%(levelname)s : %(message)s : %(asctime)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# if you need downgrading the fps per second pass this variable to the fps at the end of the main loop
snake_speed = 10

window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

game_window = pygame.display.set_mode((window_x, window_y))

#adding sound effects
eat_sound = pygame.mixer.Sound("sounds/eat.wav")
game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")

#making variable available
game_started = False

# Set font
font = pygame.font.Font(None, 30)

# Create text surface
text = font.render("Do you want to play the game?`y` `n`", True, (255, 255, 255))

# Get text rectangle
text_rect = text.get_rect()

# Center text on screen
text_rect.centerx = game_window.get_rect().centerx
text_rect.centery = game_window.get_rect().centery - 20

# Blit the text to the screen
game_window.blit(text, text_rect)

# Update the display
pygame.display.flip()

# Wait for the user to press a key
pygame.event.wait()

def main():
    """ 
    The main game loop Function
     
    """
    global game_started
    global game_window
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    # User wants to play the game
                    logging.info("User wants to play the game")
                    game_started = True
                elif event.key == pygame.K_n:
                    # User does not want to play the game
                    logging.info("USER DOESN'T want to play the GAME!")
                    pygame.quit()
                    sys.exit()
        if game_started == True:
            eat_sound = pygame.mixer.Sound("sounds/eating-effect.mp3")
            game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")

            fps = pygame.time.Clock()

            snake_position = [100, 50]
            snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

            fruit_position = [random.randrange(1, (window_x//10)) * 10,
                            random.randrange(1, (window_y//10)) * 10]

            fruit_spawn = True

            direction = 'RIGHT'
            change_to = direction

            score = 0

            def show_score(choice, color, font, size):
                score_font = pygame.font.SysFont(font, size)
                score_surface = score_font.render('Score : ' + str(score), True, color)
                score_rect = score_surface.get_rect()
                game_window.blit(score_surface, score_rect)

            def game_over():
                game_over_sound.play()

                my_font = pygame.font.SysFont('times new roman', 50)
                game_over_surface = my_font.render(
                    'Your Score is : ' + str(score), True, red)
                game_over_rect = game_over_surface.get_rect()
                game_over_rect.midtop = (window_x/2, window_y/4)
                game_window.blit(game_over_surface, game_over_rect)
                pygame.display.flip()
                time.sleep(3)
                pygame.quit()
                quit()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            change_to = 'UP'
                        if event.key == pygame.K_DOWN:
                            change_to = 'DOWN'
                        if event.key == pygame.K_LEFT:
                            change_to = 'LEFT'
                        if event.key == pygame.K_RIGHT:
                            change_to = 'RIGHT'

                if change_to == 'UP' and direction != 'DOWN':
                    direction = 'UP'
                if change_to == 'DOWN' and direction != 'UP':
                    direction = 'DOWN'
                if change_to == 'LEFT' and direction != 'RIGHT':
                    direction = 'LEFT'
                if change_to == 'RIGHT' and direction != 'LEFT':
                    direction = 'RIGHT'

                if direction == 'UP':
                    snake_position[1] -= 10
                if direction == 'DOWN':
                    snake_position[1] += 10
                if direction == 'LEFT':
                    snake_position[0] -= 10
                if direction == 'RIGHT':
                    snake_position[0] += 10

                snake_body.insert(0, list(snake_position))
                if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
                    score += 10
                    eat_sound.play()
                    fruit_spawn = False
                else:
                    snake_body.pop()

                if not fruit_spawn:
                    fruit_position = [random.randrange(1, (window_x//10)) * 10,
                                    random.randrange(1, (window_y//10)) * 10]

                fruit_spawn = True
                game_window.fill(black)

                for pos in snake_body:
                    pygame.draw.rect(game_window, green,
                                    pygame.Rect(pos[0], pos[1], 10, 10))

                pygame.draw.rect(game_window, white,
                                pygame.Rect(fruit_position[0], fruit_position[1], 10,
                                            10))

                if snake_position[0] < 0 or snake_position[0] > window_x-10: 
                    game_over()
                if snake_position[1] < 0 or snake_position[1] > window_y-10:
                    game_over()

                for block in snake_body[1:]:
                    if snake_position[0] == block[0] and snake_position[1] == block[1]:
                        game_over()

                show_score(1, white, 'times new roman', 20)

                # Display The Game Screen
                pygame.display.update()
                
                # Limit the frame rate to 60 FPS
                fps.tick(60)
                
main()

pygame.quit()