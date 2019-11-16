import TetrisGame
import pygame
import numpy as np

# Tetris piece colours
tetris_colours = [(0, 0, 0),
                  (255, 0, 0),
                  (0, 150, 0),
                  (0, 0, 255),
                  (255, 120, 0),
                  (255, 255, 0),
                  (180, 0, 255),
                  (0, 220, 220)]

# Pixel Sizes
tetris_pixel_size = 10

pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)
screen.fill((0, 100, 100))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Create game_board surface for the tetris grid
game_board_size = [i * tetris_pixel_size for i in (10, 24)]
game_surface = pygame.Surface(game_board_size)

# Create tetris game object
tetrisGame = TetrisGame.TetrisGame()

run = True
while run:
    # get and process events, including keypress
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # this method of getting keypresses does not repeat
            if event.key == pygame.K_DOWN:
                tetrisGame.move_drop()
            if event.key == pygame.K_UP:
                tetrisGame.move_rotate(1)
            if event.key == pygame.K_RIGHT:
                tetrisGame.move_horizontal(1)
            if event.key == pygame.K_LEFT:
                tetrisGame.move_horizontal(-1)
            if event.key == pygame.K_z:
                tetrisGame.move_rotate(-1)
            if event.key == pygame.K_x:
                tetrisGame.move_hold()

    # Update game object stats
    tetrisGame.game_tick()

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # --- Drawing code should go here
    # Draw the combined board
    for index_x, row_x in enumerate(tetrisGame.get_combined_board()):
        for index_y, item in enumerate(row_x):
            tetris_pixel = pygame.Rect((index_x * tetris_pixel_size, index_y * tetris_pixel_size), (tetris_pixel_size, tetris_pixel_size))
            pygame.draw.rect(game_surface, tetris_colours[item], tetris_pixel)

    # Update Screen Surface
    screen.blit(game_surface, (350, 100))
    pygame.display.flip()

    # Frame Rate Limit
    clock.tick(60)
