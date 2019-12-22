import time

import pandas as pd
import numpy as np
import os

import keras
from keras import Input, Model
from keras.layers import Dense, concatenate, Conv2D, Flatten, MaxPooling2D, Reshape

from TetrisGame import TetrisGame
from DrawBoard import DrawBoard


def prepare_model_inputs(input_dicts):
    # takes list of game_state dict - list size is the batch size, returns a list of batched elements for model input

    # define the keys for the inputs
    keys_board = ("placed_board", "combined_board", "current_tetris_board", "dropped_board")
    keys_tetris = ("current_tetris_4x4", "saved_tetris_4x4")
    keys_gaps = ("top_line_gaps", )
    keys_one_dim = ("game_tick_index",
                    "lines_cleared",
                    "pos_x",
                    "pos_y",
                    "tetris_current_width",
                    "tetris_current_height",
                    "tetris_current_width_lowest",
                    "tetris_saved_width",
                    "tetris_saved_height",
                    "tetris_saved_width_lowest",
                    "dropped_board_height_percentage",
                    "dropped_board_lines_cleared",
                    "board_fill_percentage",
                    "board_height_percentage",
                    "top_line_fill_percentage",
                    "move_hold_valid")
    # store into a list for iteration
    input_type_keys = [keys_board, keys_tetris, keys_gaps, keys_one_dim]

    # handle batch size of 0 passed as singular dict
    if type(input_dicts) == dict:
        input_dicts = [input_dicts]

    # prepare and store into list for iteration the lists for the inputs to be placed into
    board_input, tetris_input, gap_input, one_dim_input = [], [], [], []
    input_type_lists = [board_input, tetris_input, gap_input, one_dim_input]

    # separate the list of dicts into list batches of each input
    for batch_dict in input_dicts:
        for input_type_list, input_type_key in zip(input_type_lists, input_type_keys):
            input_type_list.append([batch_dict.get(i) for i in input_type_key])  # dict.get() doesnt accept lists

    # concatenate each list batch into (batchsize, ...) shape - axis 0 is the batch axis
    # reshape the inputs to have a batch axis at position 0
    input_type_lists = [np.expand_dims(i, axis=0) for i in input_type_lists]
    # concat along axis 0 to group batches up
    input_type_lists = [np.concatenate(i, axis=0) for i in input_type_lists]

    return input_type_lists


# create game instance and define action_space in list
game = TetrisGame()
action_space = [lambda: game.move_rotate(1),
                lambda: game.move_rotate(-1),
                lambda: game.move_horizontal(1),
                lambda: game.move_horizontal(-1),
                lambda: game.move_drop_hard(),
                lambda: game.move_drop_soft(1),
                lambda: game.move_hold()]

# define model, not using sequential (old)
# first_input = Input(shape=(10, 24, 1))  # placed board
# first_dense = Conv2D(240, 4, use_bias=True)(first_input)
# first_dense = MaxPooling2D()(first_dense)
# first_dense = Dense(400, )(first_dense)
# first_dense = Flatten()(first_dense)  # flatten layer needed to convert 4d into 2d
#
# second_input = Input(shape=(4, 4, 1))  # current piece
# second_dense = Conv2D(16, 2, use_bias=True)(second_input)
# second_dense = MaxPooling2D()(second_dense)
# second_dense = Dense(100, )(second_dense)
# second_dense = Flatten()(second_dense)  # flatten layer needed to convert 4d into 2d
#
# merge_one = concatenate([first_dense, second_dense])
# merge_one = Dense(350)(merge_one)
#
# third_input = Input(shape=(5, ))  # single dim values
# third_dense = Dense(200, )(third_input)
# merge_two = concatenate([merge_one, third_dense])
#
# output = Dense(4)(merge_two)
#
# model = Model(inputs=[first_input, second_input, third_input], outputs=output)
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# model.summary()

# define model using functional api
# inputs
in_boards = Input(shape=(4, 10, 24), name="in_boards")  # placed, combined, current_tetris, dropped - boards
in_tetris = Input(shape=(2, 4, 4), name="in_tetris")  # current_tetris_4x4, saved_tetris_4x4
in_gaps = Input(shape=(1, 10), name="in_gaps")  # top_line_gaps, technically a one dimensional input
in_one_dim = Input(shape=(16, ), name="in_one_dim")  # other one dimensional inputs

# model layers
layer_boards = Dense(100)(in_boards)
layer_tetris = Dense(100)(in_tetris)
layer_gaps = Dense(10)(in_gaps)

# reshape and dense to match shapes
layer_boards = Reshape(target_shape=(100, 40))(layer_boards)
layer_tetris = Reshape(target_shape=(40, 20))(layer_tetris)
layer_gaps = Reshape(target_shape=(10, 1))(layer_gaps)

layer_boards = Dense(100)(layer_boards)
layer_tetris = Dense(100)(layer_tetris)
layer_gaps = Dense(100)(layer_gaps)

# combine the multi_dim layers
layer_multi_dim = concatenate([layer_boards, layer_tetris, layer_gaps], axis=1)
layer_multi_dim = Dense(1000)(layer_multi_dim)

# handle single dim layer
layer_one_dim = Dense(100)(in_one_dim)

# reshape and combine the multi_dim and the single dim layers
layer_multi_dim = Flatten()(layer_multi_dim)
layer_main = concatenate([layer_one_dim, layer_multi_dim])
layer_main = Dense(1000)(layer_main)
layer_main = Dense(1000)(layer_main)

# outputs - corresponding to actions in the action space
output = Dense(len(action_space), name="output", activation="relu")(layer_main)

# compile model
model = Model(inputs=[in_boards, in_tetris, in_gaps, in_one_dim], outputs=output)
model.compile(loss='mse', optimizer='adam')
model.summary()

# load model
# dir_str = "tetris_dqn_training/tetris_dqn_models"
# dir_files = os.listdir(dir_str)
# model = keras.models.load_model(dir_str + "/" + dir_files[-1])
# model.summary()

# Training Hyper-Parameters
epoch_total = 100
# how often the model's move is used versus a random move
mutate_threshold = 0.5  # 0 = all model moves, 1 = all random moves
draw_board = False  # display training actions on screen

# training start
reward_list, inputs_list, action_taken_list, game_tick_index_list, lines_cleared_list = [], [], [], [], []
epoch = 0
time_start = time.time()
continue_train = True
if draw_board:
    drawBoard = DrawBoard()

while continue_train:
    # get and store the game_state
    game_state = game.get_state()
    inputs_list.append(game_state)

    # here decide whether or not to use the model prediction or a random prediction to help the model improve
    if np.random.rand() > mutate_threshold:
        # make and store a predicted action, reshape to add batch size of 1
        action_proba = model.predict(prepare_model_inputs(game_state))
        action_taken_list.append(action_proba[0])
    else:
        # randomly select and store an action
        action_to_take = np.random.randint(len(action_space))
        action_proba = np.zeros(len(action_space))
        action_proba[action_to_take] = 1
        action_taken_list.append(action_proba)

    # do the lowest value action and tick the game
    action_space[int(np.argmin(action_proba))]()
    game.game_tick()

    # draw the board
    if draw_board:
        drawBoard.draw_board(game_state[0])
        drawBoard.draw_board(game.get_combined_board())

    # store the reward for training - minimise
    reward_list.append(game_state.get("board_height_percentage"))

    # check if game is over and fit the model
    if not game.game_live:
        # convert action list to have the actual reward given
        reward_list.insert(0, 0)  # reward of 0 for first item
        action_taken_list = np.array(action_taken_list)
        for index, row in enumerate(action_taken_list):
            row[np.argmin(row)] = reward_list[index+1]

        # fit the model
        model.fit(prepare_model_inputs(inputs_list), action_taken_list, verbose=1)

        # reset the training data lists
        reward_list, inputs_list, action_taken_list = [], [], []

        # log progress
        epoch += 1
        print("Epoch: {}, GameTicks: {}, LinesCleared: {}, EstTimeRemaining(s): {}".format(epoch,
                                                                                           game.game_tick_index,
                                                                                           game.lines_cleared,
                                                                                           ((time.time() - time_start) / (1 - ((epoch_total - epoch) / epoch_total))) - (time.time() - time_start)))
        game_tick_index_list.append(game.game_tick_index)
        lines_cleared_list.append(game.lines_cleared)

        # finish training if epoch limit is reached, otherwise reset the game for another epoch
        if epoch == epoch_total:
            continue_train = False
        else:
            game.game_reset()


print("-- Training Finished -- ")

print("Average Ticks Survived: {} Average Lines Cleared: {}".format(np.average(game_tick_index_list),
                                                                    np.average(lines_cleared_list)))
print("Max Ticks Survived: {} Max Lines Cleared: {}".format(np.max(game_tick_index_list),
                                                            np.max(lines_cleared_list)))

# save model and training data
files_list = os.listdir("tetris_dqn_training/tetris_dqn_models")
files_list.sort(key=lambda x:int(x.split("_")[0]))

# check if there are existing save entries
if len(files_list) == 0:
    epoch_start = 0
    file_index = 0
else:
    file_index = int(files_list[-1].split("_")[0]) + 1
    epoch_start = int(files_list[-1].split("_")[-1].split(".h5")[0])

epoch_end = epoch_start + epoch
model.save("tetris_dqn_training/tetris_dqn_models/{}_tetris_dqn_model_{}_{}.h5".format(file_index, epoch_start, epoch_end))
pd.DataFrame([game_tick_index_list, lines_cleared_list]).to_csv("tetris_dqn_training/tetris_dqn_progress/{}_tetris_dqn_progress_{}_{}.csv".format(file_index, epoch_start, epoch_end), index=False)

