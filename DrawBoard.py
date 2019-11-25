import pygame


class DrawBoard(object):

    # Tetris piece colours
    tetris_colours = [(0, 0, 0),
                      (255, 0, 0),
                      (0, 150, 0),
                      (0, 0, 255),
                      (255, 120, 0),
                      (255, 255, 0),
                      (180, 0, 255),
                      (0, 220, 220)]

    def __init__(self, size_screen=(700, 500), size_board=(10, 24)):
        pygame.init()
        pygame.display.set_caption("Tetris Training Progress Display")

        self.screen = pygame.display.set_mode(size_screen)
        self.screen.fill((0, 100, 100))

        self.tetris_pixel_size = 20

        # Create game_board surface for the tetris grid
        self.game_board_size = [i * self.tetris_pixel_size for i in size_board]
        self.surface_board = pygame.Surface(self.game_board_size)

    def draw_board(self, board_array):
        # Draw the combined board on the surface_board
        for index_x, row_x in enumerate(board_array):
            for index_y, item in enumerate(row_x):
                tetris_pixel = pygame.Rect((index_x * self.tetris_pixel_size, index_y * self.tetris_pixel_size),
                                           (self.tetris_pixel_size, self.tetris_pixel_size))
                pygame.draw.rect(self.surface_board, self.tetris_colours[item], tetris_pixel)

        self.screen.blit(self.surface_board, (250, 10))
        pygame.display.flip()
