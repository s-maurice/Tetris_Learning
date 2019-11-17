import time
import pygame

# quick way to draw placed_board printouts

# Tetris piece colours
tetris_colours = [(0, 0, 0),
                  (255, 0, 0),
                  (0, 150, 0),
                  (0, 0, 255),
                  (255, 120, 0),
                  (255, 255, 0),
                  (180, 0, 255),
                  (0, 220, 220),
                  (128, 128, 128)]

board = [[0, 0, 4, 0, 0, 0, 2, 2, 2, 2, 6, 6, 6, 6, 4, 0, 1, 1, 1, 7, 7, 4, 0, 0]
, [0, 0, 4, 4, 4, 2, 2, 2, 2, 0, 0, 0, 0, 0, 4, 4, 4, 1, 0, 7, 7, 4, 4, 4]
, [0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6]
, [2, 2, 3, 3, 0, 7, 7, 0, 0, 5, 0, 0, 5, 6, 6, 6, 6, 6, 6, 6, 6, 3, 3, 0]
, [0, 0, 0, 3, 3, 7, 7, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3]
, [0, 0, 3, 3, 0, 0, 0, 5, 3, 3, 6, 6, 6, 6, 5, 0, 0, 5, 0, 0, 5, 3, 3, 0]
, [0, 0, 5, 3, 3, 5, 5, 5, 0, 3, 3, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 3, 3]
, [5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
, [0, 0, 4, 0, 3, 3, 6, 6, 6, 6, 4, 0, 3, 3, 6, 6, 6, 6, 5, 0, 2, 2, 0, 5]
, [0, 0, 4, 4, 4, 3, 3, 0, 0, 0, 4, 4, 4, 3, 3, 0, 5, 5, 5, 2, 2, 5, 5, 5]]

pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)
screen.fill((0, 100, 100))
pygame.display.set_caption("Tetris")

tetris_pixel_size = 20
# Create game_board surface for the tetris grid
game_board_size = [i * tetris_pixel_size for i in (10, 24)]
surface_board = pygame.Surface(game_board_size)

# Draw the combined board on the surface_board
for index_x, row_x in enumerate(board):
    for index_y, item in enumerate(row_x):
        tetris_pixel = pygame.Rect((index_x * tetris_pixel_size, index_y * tetris_pixel_size),
                                   (tetris_pixel_size, tetris_pixel_size))
        pygame.draw.rect(surface_board, tetris_colours[item], tetris_pixel)

screen.blit(surface_board, (250, 10))
pygame.display.flip()
time.sleep(5)