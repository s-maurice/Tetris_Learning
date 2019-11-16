import pygame
import numpy as np


# Create a game board, 10x24 with 10x20 showing
game_board = np.zeros((10, 24), dtype=int)
test_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6],  # Bottom left
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]  # Bottom Right

test_board = np.array(test_board)

# Tetris piece colours
tetris_colours = [(0, 0, 0),
                  (255, 0, 0),
                  (0, 150, 0),
                  (0, 0, 255),
                  (255, 120, 0),
                  (255, 255, 0),
                  (180, 0, 255),
                  (0, 220, 220)]

# Tetris piece shapes
tetris_shapes = [[[1, 1, 1],
                  [0, 1, 0]],

                 [[0, 2, 2],
                  [2, 2, 0]],

                 [[3, 3, 0],
                  [0, 3, 3]],

                 [[4, 0, 0],
                  [4, 4, 4]],

                 [[0, 0, 5],
                  [5, 5, 5]],

                 [[6, 6, 6, 6]],

                 [[7, 7],
                  [7, 7]]]


def combine_board(board, shape, shape_pos):
    # add to board, testing for collision
    # returns False if move is illegal, else returns combined board
    for index_x, row_x in enumerate(shape):
        for index_y, item in enumerate(row_x):
            if (item != 0) and (board[shape_pos[0] + index_x, shape_pos[1] + index_y] != 0):
                return False
            else:
                board[shape_pos[0] + index_x, shape_pos[1] + index_y] = item
    return board


# Try adding tetris_shape to test_board
combined_board = combine_board(test_board.copy(), tetris_shapes[0], (7, 5))
print(combined_board)

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
