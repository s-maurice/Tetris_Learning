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
        self.game_tick_index = 0
        self.ticks_per_movedown = 20
        self.game_live = True

        # Player Position
        self.pos = [int(self.board_size[0] / 2), 0]
        self.current_tetris = self.get_random_tetris()
        self.upcoming_tetris_list = [self.get_random_tetris() for _ in range(5)]
        self.upcoming_tetris_list = [self.tetris_shapes[5] for _ in range(5)]  # Debug

    def get_combined_board(self):
        # Blindly combines board, placing current_tetris on top
        combined_board = self.placed_board.copy()  # Start with combined_board
        for cur_tetris_index_x, row_x in enumerate(self.current_tetris):
            for cur_tetris_index_y, item in enumerate(row_x):
                if not item == 0:
                    combined_board[self.pos[0] + cur_tetris_index_x, self.pos[1] + cur_tetris_index_y] = item
        return combined_board

    def is_collision(self, check_tetris, check_pos):
        # returns true if move is illegal or out of range
        # first catch if the check_pos overflows the board sides
        if check_pos[0] < 0 or check_pos[0] > self.board_size[0]-1:
            return True
        # check for collision between check_tetris and placed_board
        for cur_tetris_index_x, row_x in enumerate(check_tetris):
            for cur_tetris_index_y, item in enumerate(row_x):
                try:
                    if (item != 0) and (self.placed_board[check_pos[0] + cur_tetris_index_x, check_pos[1] + cur_tetris_index_y] != 0):
                        return True
                except IndexError:
                    # catches indexerror for "I" blocks on the right side of board
                    return True
        return False

    def get_random_tetris(self):
        return self.tetris_shapes[np.random.randint(7)]

    def get_next_block(self):
        # Replenish upcoming_tetris_list with new tetris
        self.upcoming_tetris_list.append(self.get_random_tetris())
        # Return and remove first item from upcoming_tetris_list
        return self.upcoming_tetris_list.pop(0)

    def move_down(self):
        # moves position one block down, checking if block is placed
        # block is placed if there is a collision is pos_y + 1
        if self.is_collision(self.current_tetris, (self.pos[0], self.pos[1] + 1)):
            # Place current block onto the placed_board
            self.placed_board = self.get_combined_board()
            # Get a new block and reset to top of screen
            # be aware of bug caused by overhangs that may mean
            # new block is placed into existing blocks or invalid position
            self.current_tetris = self.get_next_block()

            # check for valid positions at top of screen, return blank to skip over game over
            for try_offset in range(self.board_size[0]):
                if not self.is_collision(self.current_tetris, (self.pos[0] + try_offset, 0)):
                    self.pos[0] += try_offset
                    self.pos[1] = 0
                    return
                elif not self.is_collision(self.current_tetris, (self.pos[0] - try_offset, 0)):
                    self.pos[0] -= try_offset
                    self.pos[1] = 0
                    return
            # game over if no valid position at pos[1] = 0
            print("Game Over")
            self.game_live = False
        else:
            self.pos[1] += 1

    def move_horizontal(self, movement_x):
        # Do movement only if valid
        if not self.is_collision(self.current_tetris, (self.pos[0] + movement_x, self.pos[1])):
            self.pos[0] += movement_x

    def move_drop(self):
        # Drop current_tetris to lowest position checking for collision for all blocks below
        # use for loop to check is_collision until collision or simply call move_down mu
        for drop_y in range(self.pos[1], self.board_size[1]):
            # Possibly board_size -1 / may call move_down too much
            if not self.is_collision(self.current_tetris, (self.pos[0], drop_y)):
                self.move_down()

    def move_rotate(self, rotation_direction):
        # rotate current_tetris
        # rotation_direction: 1 or -1, amount of times to rotate the matrix by 90deg
        # check for collision on a copy before rotating
        if not self.is_collision(np.rot90(self.current_tetris.copy(), rotation_direction), self.pos):
            self.current_tetris = np.rot90(self.current_tetris, rotation_direction)
        else:
            # if rotating would be illegal, check position 1 and 2 blocks to the left and right
            # check check order depending on rotation_direction / doesn't really matter, just check 1 before 2
            check_pos_offset_list = [1, -1]
            # special case for "I" blocks, append -3 to list
            # np.array_equiv returns true if one can be broadcast to another
            if np.array_equiv(self.current_tetris, self.tetris_shapes[5]):
                check_pos_offset_list.append(-3)
            for pos_offset in check_pos_offset_list:
                if not self.is_collision(np.rot90(self.current_tetris.copy(), rotation_direction), (self.pos[0] + pos_offset, self.pos[1])):
                    self.current_tetris = np.rot90(self.current_tetris, rotation_direction)
                    self.pos[0] += pos_offset
                    break

    def clear_rows(self):
        # remove completed rows from placed_board
        for row_index, row in enumerate(np.transpose(self.placed_board)):
            if 0 not in row:
                self.placed_board = np.delete(self.placed_board, row_index, axis=1)
                self.placed_board = np.insert(self.placed_board, 0, np.zeros(self.board_size[0]), axis=1)

    def game_tick(self):
        if self.game_live:
            self.game_tick_index += 1
            self.clear_rows()
            if self.game_tick_index % self.ticks_per_movedown == 0:
                self.move_down()
