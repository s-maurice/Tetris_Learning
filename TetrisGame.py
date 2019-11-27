import numpy as np


class TetrisGame(object):
    # Tetris piece colours - not needed here
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
        self.ticks_per_movedown = 10  # usually 30
        self.lines_cleared = 0
        self.game_live = True

        # Player Position
        self.pos = [int(self.board_size[0] / 2), 0]
        self.current_tetris = self.get_random_tetris()
        self.upcoming_tetris_list = [self.get_random_tetris() for _ in range(5)]
        # self.upcoming_tetris_list = [self.tetris_shapes[5] for _ in range(5)]  # Debug
        self.saved_tetris = None
        self.move_hold_valid = True

    def get_combined_board(self):
        # Blindly combines board, placing current_tetris on top
        combined_board = self.placed_board.copy()  # Start with combined_board
        try:
            for cur_tetris_index_x, row_x in enumerate(self.current_tetris):
                for cur_tetris_index_y, item in enumerate(row_x):
                    if not item == 0:
                        combined_board[self.pos[0] + cur_tetris_index_x, self.pos[1] + cur_tetris_index_y] = item
        except IndexError:
            # this means a move is illegal - catch for drawing methods still draw the board without checking validity
            return self.placed_board
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
                    # catches IndexError for "I" blocks on the right side of board
                    return True
        return False

    def get_random_tetris(self):
        return self.tetris_shapes[np.random.randint(7)]

    def get_next_block(self):
        # Replenish upcoming_tetris_list with new tetris
        self.upcoming_tetris_list.append(self.get_random_tetris())
        # Return and remove first item from upcoming_tetris_list
        return self.upcoming_tetris_list.pop(0)

    def move_hold(self):
        # check if swap is allowed
        if self.move_hold_valid:
            # saves or swaps the saved block
            if self.saved_tetris is None:
                # handle empty saved_tetris case
                # check if position at top is valid before swapping or moving
                if self.move_reset_tetris_position(self.upcoming_tetris_list[0]):
                    self.saved_tetris = self.current_tetris
                    self.current_tetris = self.get_next_block()
            else:
                # swap current_tetris and saved_tetris
                # check if position at top is valid before swapping or moving
                if self.move_reset_tetris_position(self.saved_tetris):
                    self.current_tetris, self.saved_tetris = self.saved_tetris, self.current_tetris
            self.move_hold_valid = False

    def move_reset_tetris_position(self, check_tetris):
        # moves the player position to the top of the board, searching for valid positons
        # if valid position if found, moves position and returns true
        # if no valid position is found, doesnt move position and returns false
        for try_offset in range(self.board_size[0]):
            if not self.is_collision(check_tetris, (self.pos[0] + try_offset, 0)):
                self.pos[0] += try_offset
                self.pos[1] = 0
                return True
            elif not self.is_collision(check_tetris, (self.pos[0] - try_offset, 0)):
                self.pos[0] -= try_offset
                self.pos[1] = 0
                return True
        return False

    def move_down(self):
        # moves position one block down, checking if block is placed
        # block is placed if there is a collision is pos_y + 1
        if self.is_collision(self.current_tetris, (self.pos[0], self.pos[1] + 1)):
            # Place current block onto the placed_board
            self.placed_board = self.get_combined_board()
            # Get a new block
            self.current_tetris = self.get_next_block()
            # Reset move_hold_valid
            self.move_hold_valid = True
            # Try to move to top of board, game over if no valid position
            if not self.move_reset_tetris_position(self.current_tetris):
                # game over if no valid position at pos[1] = 0
                print("Game Over")
                self.game_live = False
        else:
            self.pos[1] += 1

    def move_horizontal(self, movement_x):
        # Do movement only if valid
        if not self.is_collision(self.current_tetris, (self.pos[0] + movement_x, self.pos[1])):
            self.pos[0] += movement_x

    def move_drop_soft(self, n_drop):
        # Drop current_tetris n_drop blocks
        [self.move_down() for _ in range(n_drop)]

    def move_drop_hard(self):
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
                self.lines_cleared += 1

    def game_tick(self):
        if self.game_live:
            self.game_tick_index += 1
            self.clear_rows()  # clear_rows here will clear the blocks quickly
            if self.game_tick_index % self.ticks_per_movedown == 0:
                # self.clear_rows()  # clear_rows  here will display the blocks for a few moments before removal
                self.move_down()

    def get_board_fill(self, board):
        # returns how many blocks on the placed_board are filled
        return np.count_nonzero(board)

    def get_board_fill_percentage(self, board):
        # returns the percentage of the placed_board that is filled
        return self.get_board_fill(board) / board.size

    def get_board_height(self, board):
        # returns the height index of the highest piece on the placed_board
        max_height = 0
        for row_x in board:
            row_x_height = len([item for item in row_x if item != 0])
            if row_x_height > max_height:
                max_height = row_x_height
        return max_height

    def get_board_height_percentage(self, board):
        return self.get_board_height(board) / self.board_size[1]

    def get_top_line_gaps(self):
        # returns a 1xWidth slice of the top board line containing placed items
        # 1 = empty spot, 0 = occupied by a placed tetris
        top_line_index = self.get_board_height(self.placed_board)
        if top_line_index == 0:
            # return a fully empty slice
            top_line_slice = np.zeros(self.board_size[0], dtype="int")
        else:
            top_line_slice = self.placed_board.copy()[:, self.board_size[1] - top_line_index]
        top_line_slice[top_line_slice >= 1] = 1  # set all colours to 1
        top_line_slice = 1 - top_line_slice  # invert
        return top_line_slice

    def receive_attack(self, gap_pos):
        # adds attack line at top of placed_board with a gap at gap_pos
        # if gap_pos is None, no gap is given to the attack line, making it un-clearable
        # check if top row contains items
        if sum(self.placed_board[:, 0]) != 0:
            print("Game Over: Attacked")
            self.game_live = False
        else:
            # create row to insert
            attack_row = np.full(self.board_size[0], 8)
            attack_row[gap_pos] = 0
            self.placed_board = np.insert(self.placed_board, self.placed_board.shape[1], attack_row, axis=1)
            self.placed_board = np.delete(self.placed_board, 0, axis=1)

    def get_state(self):
        # returns list of game state, including:
        # self.placed_board
        # self.game_tick_index
        # self.lines_cleared
        # self.pos
        # self.current_tetris
        # self.upcoming_tetris_list
        # self.saved_tetris
        # self.move_hold_valid
        #
        # self.get_board_fill()
        # self.get_board_fill_percentage()
        # self.get_board_height()

        # convert current_tetris into (4, 4) shape for consistant shape
        # create a 4x4 shape array of zeros and place the shape in
        current_tetris_4x4 = np.zeros((4, 4), dtype=int)
        current_tetris_4x4[:np.array(self.current_tetris).shape[0], :np.array(self.current_tetris).shape[1]] = self.current_tetris
        # convert values to ones
        current_tetris_4x4[current_tetris_4x4 >= 1] = 1
        # TODO make tetris_to_4x4 func, for future purpose of converting the whole upcoming list
        # do the same to saved_tetris
        saved_tetris_4x4 = np.zeros((4, 4), dtype=int)
        if self.saved_tetris is not None:
            saved_tetris_4x4[:np.array(self.saved_tetris).shape[0], :np.array(self.saved_tetris).shape[1]] = self.saved_tetris
            # convert values to ones
            saved_tetris_4x4[saved_tetris_4x4 >= 1] = 1

        # convert values in placed_board to ones
        placed_board = self.placed_board.copy()
        placed_board[placed_board >= 1] = 1
        
        # create a board with the board shape with only the current tetris
        current_tetris_board = np.zeros(self.board_size, dtype=int)
        for cur_tetris_index_x, row_x in enumerate(self.current_tetris):
            for cur_tetris_index_y, item in enumerate(row_x):
                current_tetris_board[self.pos[0] + cur_tetris_index_x, self.pos[1] + cur_tetris_index_y] = 1

        # create synthetics for width and height of the current piece and saved piece and rotation
        # create synthetics for the width of the lowest block of the current and saved piece
        tetris_current_width = len(self.current_tetris)  # width
        tetris_current_height = len(self.current_tetris[0])  # height
        tetris_current_width_lowest = sum([i > 0 for i in np.array(self.current_tetris)[:, -1]])

        if self.saved_tetris is not None:
            tetris_saved_width = len(self.saved_tetris)
            tetris_saved_height = len(self.saved_tetris[0])
            tetris_saved_width_lowest = sum([i > 0 for i in np.array(self.saved_tetris)[:, -1]])
        else:
            tetris_saved_width = 0
            tetris_saved_height = 0
            tetris_saved_width_lowest = 0

        # create synthetic to show board if current block is immediately placed
        # create synthetic to show the height of the resultant board
        # create synthetic to show if placing a block would clear a line
        # code modified from move_drop_hard and get_combined_board
        dropped_board_lines_cleared = 0
        for drop_y in range(self.pos[1], self.board_size[1]):
            if self.is_collision(self.current_tetris, (self.pos[0], drop_y + 1)):
                # combine boards here - use copy of placed_board with all 1s and 0s, and insert 1s
                dropped_board = placed_board.copy()
                for cur_tetris_index_x, row_x in enumerate(self.current_tetris):
                    for cur_tetris_index_y, item in enumerate(row_x):
                        if not item == 0:
                            dropped_board[self.pos[0] + cur_tetris_index_x, drop_y + cur_tetris_index_y] = 1
                            dropped_board_height_percentage = self.get_board_height_percentage(dropped_board)
                            for row in dropped_board:
                                if 0 not in row:
                                    dropped_board_lines_cleared += 1
                break

        # convert move_hold_valid into 1 or 0
        move_hold_valid = 1 if self.move_hold_valid else 0

        state_dict = dict(placed_board=placed_board.tolist(),
                          combined_board=self.get_combined_board(),
                          current_tetris_board=current_tetris_board,
                          game_tick_index=self.game_tick_index,
                          lines_cleared=self.lines_cleared,
                          pos_x=self.pos[0],
                          pos_y=self.pos[1],
                          tetris_current_width=tetris_current_width,
                          tetris_current_height=tetris_current_height,
                          tetris_current_width_lowest=tetris_current_width_lowest,
                          tetris_saved_width=tetris_saved_width,
                          tetris_saved_height=tetris_saved_height,
                          tetris_saved_width_lowest=tetris_saved_width_lowest,
                          current_tetris_4x4=current_tetris_4x4,
                          saved_tetris_4x4=saved_tetris_4x4,
                          dropped_board=dropped_board,
                          dropped_board_height_percentage=dropped_board_height_percentage,
                          dropped_board_lines_cleared=dropped_board_lines_cleared,
                          # upcoming_tetris_list = self.upcoming_tetris_list,  # don't use this yet
                          move_hold_valid=move_hold_valid,
                          top_line_gaps=self.get_top_line_gaps(),
                          top_line_fill_percentage=self.get_board_fill_percentage(1 - self.get_top_line_gaps()),
                          board_fill_percentage=self.get_board_fill_percentage(self.placed_board),
                          board_height_percentage=self.get_board_height_percentage(self.placed_board))

        return [placed_board.tolist(),
                # self.game_tick_index,
                self.lines_cleared,
                self.pos[0],
                self.pos[1],
                # tetris_current_width,
                # tetris_current_height,
                # tetris_current_width_lowest,
                # tetris_saved_width,
                # tetris_saved_height,
                # tetris_saved_width_lowest,
                current_tetris_4x4,
                # saved_tetris_4x4,
                # dropped_board,
                # dropped_board_height_percentage,
                # dropped_board_lines_cleared,
                # self.upcoming_tetris_list,  # don't use this yet
                # move_hold_valid
                # self.get_top_line_gaps(),
                self.get_board_fill_percentage(self.placed_board),
                self.get_board_height_percentage(self.placed_board)]

    def game_reset(self):
        self.__init__()
