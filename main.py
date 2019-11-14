import TetrisGame
import pygame
import numpy as np

# Pixel Sizes
tetris_pixel_size = 10

pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)
screen.fill((0, 100, 100))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Create game_board surface for the tetris grid
game_board_size = [i * tetris_pixel_size for i in test_board.shape]
game_surface = pygame.Surface(game_board_size)

run = True
while run:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # --- Drawing code should go here
    # Draw the combined board
    for index_x, row_x in enumerate(combined_board):
        for index_y, item in enumerate(row_x):
            tetris_pixel = pygame.Rect((index_x * tetris_pixel_size, index_y * tetris_pixel_size), (tetris_pixel_size, tetris_pixel_size))
            pygame.draw.rect(game_surface, tetris_colours[item], tetris_pixel)

    # Update Screen Surface
    screen.blit(game_surface, (350, 100))
    pygame.display.flip()

    # Frame Rate Limit
    clock.move_down(60)
