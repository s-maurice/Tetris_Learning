import numpy as np


class TetrisGame(object):
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

    def __init__(self):
        # Board State
        self.board_size = (10, 24)
        self.placed_board = np.zeros(self.board_size, dtype=int)
        self.current_tetris = self.get_random_tetris()
        self.upcoming_tetris_list = [self.get_random_tetris() for _ in range(5)]

        # Player Position
        self.pos = [self.board_size[0] / 2, 0]

    def get_combined_board(self):
        # Blindly combines board, placing current_tetris on top
        combined_board = self.placed_board.copy()  # Start with combined_board
        for cur_tetris_index_x, row_x in enumerate(self.current_tetris):
            for cur_tetris_index_y, item in enumerate(row_x):
                combined_board[self.pos[0] + cur_tetris_index_x, self.pos[1] + cur_tetris_index_y] = item
        return combined_board

    def is_collision(self, check_pos):
        # returns true if move is illegal or out of range
        for cur_tetris_index_x, row_x in enumerate(self.current_tetris):
            for cur_tetris_index_y, item in enumerate(row_x):
                try:
                    if (item != 0) and (self.placed_board[check_pos[0] + cur_tetris_index_x, check_pos[1] + cur_tetris_index_y] != 0):
                        return True
                except IndexError:
                    # Index error returns out of range
                    print("DEBUG: IndexError in is_collision - position out of game boundary.")
                    return True
        return False

    def get_random_tetris(self):
        return self.tetris_shapes[np.random.randint(7)]

    def get_next_block(self):
        # Replenish upcoming_tetris_list with new tetris
        self.upcoming_tetris_list[-1] = self.get_random_tetris()
        # Return and remove first item from upcoming_tetris_list
        return self.upcoming_tetris_list.pop(0)

    def move_down(self):
        # moves position one block down, checking if block is placed
        self.pos[1] += 1
        # block is placed if there is a collision is pos_y + 1
        if self.is_collision((self.pos[0], self.pos[1] + 1)):
            # Place current block onto the placed_board
            self.placed_board = self.get_combined_board()
            # Get a new block and reset to top of screen
            # be aware of bug caused by overhangs that may mean new block is placed into existing blocks
            self.current_tetris = self.get_next_block()
            self.pos[1] = 0

    def move_horizontal(self, movement_x):
        # Do movement only if valid
        if not self.is_collision((self.pos[0] + movement_x, self.pos[1])):
            self.pos[0] += movement_x

    def move_drop(self):
        # Drop current_tetris to lowest position checking for collision for all blocks below
        # use for loop to check is_collision until collision or simply call move_down mu
        for drop_y in range(self.pos[1], self.board_size[1]):  # Possibly board_size -1 / may call move_down too much
            if self.is_collision((self.pos[0], drop_y)):
                self.move_down()
