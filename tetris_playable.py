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
                  (0, 220, 220),
                  (128, 128, 128)]

# Pixel Sizes
tetris_pixel_size = 20
upcoming_tetris_display_gap = 10

pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)
screen.fill((0, 100, 100))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Create game_board surface for the tetris grid
game_board_size = [i * tetris_pixel_size for i in (10, 24)]
surface_board = pygame.Surface(game_board_size)
surface_saved = pygame.Surface((4 * tetris_pixel_size, 4 * tetris_pixel_size))
surface_upcoming = pygame.Surface(((2 * tetris_pixel_size), ((4 * tetris_pixel_size * 5) + upcoming_tetris_display_gap * 5)))
surface_upcoming.fill((0, 100, 100))

# Create font for text
text_font = pygame.font.SysFont('Comic Sans MS', 16)

# Create tetris game object
tetrisGame = TetrisGame.TetrisGame()

run = True
while run:
    # Get and process events, including keypress
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # this method of getting keypresses does not repeat
            if event.key == pygame.K_DOWN:
                tetrisGame.move_drop_soft(1)
            if event.key == pygame.K_UP:
                tetrisGame.move_rotate(1)
            if event.key == pygame.K_RIGHT:
                tetrisGame.move_horizontal(1)
            if event.key == pygame.K_LEFT:
                tetrisGame.move_horizontal(-1)
            if event.key == pygame.K_SPACE:
                tetrisGame.move_drop_hard()
            if event.key == pygame.K_z:
                tetrisGame.move_rotate(-1)
            if event.key == pygame.K_x:
                tetrisGame.move_hold()
            if event.key == pygame.K_d:
                tetrisGame.receive_attack(5)  # debug
            if event.key == pygame.K_e:
                tetrisGame.get_state()
                # print(tetrisGame.get_top_line_gaps())  # debug

    # Update game object status
    tetrisGame.game_tick()

    # Draw the combined board on the surface_board
    for index_x, row_x in enumerate(tetrisGame.get_combined_board()):
        for index_y, item in enumerate(row_x):
            tetris_pixel = pygame.Rect((index_x * tetris_pixel_size, index_y * tetris_pixel_size), (tetris_pixel_size, tetris_pixel_size))
            pygame.draw.rect(surface_board, tetris_colours[item], tetris_pixel)

    # Draw the saved block on the surface_saved
    if tetrisGame.saved_tetris is not None:
        # create a 4x4 shape array of zeros and place the shape in
        draw_saved_tetris = np.zeros((4, 4), dtype=int)
        draw_saved_tetris[:np.array(tetrisGame.saved_tetris).shape[0], :np.array(tetrisGame.saved_tetris).shape[1]] = tetrisGame.saved_tetris

        for index_x, row_x in enumerate(draw_saved_tetris.tolist()):
            for index_y, item in enumerate(row_x):
                tetris_pixel = pygame.Rect((index_x * tetris_pixel_size, index_y * tetris_pixel_size), (tetris_pixel_size, tetris_pixel_size))
                pygame.draw.rect(surface_saved, tetris_colours[item], tetris_pixel)

    # Draw the upcoming blocks
    for upcoming_index, upcoming_tetris in enumerate(tetrisGame.upcoming_tetris_list):

        # create a 2x4 shape array of zeros and place the shape in
        draw_upcoming_tetris = np.zeros((2, 4), dtype=int)
        draw_upcoming_tetris[:np.array(upcoming_tetris).shape[0], :np.array(upcoming_tetris).shape[1]] = upcoming_tetris

        upcoming_gap_offset = (upcoming_index * upcoming_tetris_display_gap) + (upcoming_index * tetris_pixel_size * 4)
        for index_x, row_x in enumerate(draw_upcoming_tetris):
            for index_y, item in enumerate(row_x):
                tetris_pixel = pygame.Rect((index_x * tetris_pixel_size, (index_y * tetris_pixel_size) + upcoming_gap_offset), (tetris_pixel_size, tetris_pixel_size))
                pygame.draw.rect(surface_upcoming, tetris_colours[item], tetris_pixel)

    # Draw text
    text_time = text_font.render("Time: " + str(tetrisGame.game_tick_index), True, (0, 0, 0), (0, 100, 100))
    text_lines_cleared = text_font.render("Lines Cleared: " + str(tetrisGame.lines_cleared), True, (0, 0, 0), (0, 100, 100))
    text_board_height = text_font.render("Board Height: " + str(tetrisGame.get_board_height(tetrisGame.placed_board)), True, (0, 0, 0), (0, 100, 100))
    text_board_fill = text_font.render("Board Fill: " + str(tetrisGame.get_board_fill(tetrisGame.placed_board)), True, (0, 0, 0), (0, 100, 100))
    text_board_fill_percentage = text_font.render("Board Fill %: " + str(round(tetrisGame.get_board_fill_percentage(tetrisGame.placed_board), 3)), True, (0, 0, 0), (0, 100, 100))
    text_pos = text_font.render("Position: " + str(tetrisGame.pos), True, (0, 0, 0), (0, 100, 100))

    # Update screen surface
    screen.blit(surface_board, (250, 10))
    screen.blit(surface_saved, (150, 10))
    screen.blit(surface_upcoming, (475, 10))
    # Update screen surface with text
    screen.blit(text_time, (100, 20 + 4 * tetris_pixel_size))
    screen.blit(text_lines_cleared, (100, 40 + 4 * tetris_pixel_size))
    screen.blit(text_board_height, (100, 60 + 4 * tetris_pixel_size))
    screen.blit(text_board_fill, (100, 80 + 4 * tetris_pixel_size))
    screen.blit(text_board_fill_percentage, (100, 100 + 4 * tetris_pixel_size))
    screen.blit(text_pos, (100, 120 + 4 * tetris_pixel_size))

    pygame.display.flip()

    # Frame rate limit
    clock.tick(60)
