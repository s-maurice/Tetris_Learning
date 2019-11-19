import time

import keras
import pandas as pd
import os

from keras import Input, Model
from keras.layers import Dense, concatenate, Conv2D, Flatten, MaxPooling2D
import numpy as np
import matplotlib.pyplot as plt

from TetrisGame import TetrisGame

game = TetrisGame()
action_space = [lambda: game.move_rotate(1),
                lambda: game.move_horizontal(1),
                lambda: game.move_horizontal(-1),
                lambda: game.move_drop_hard()]

# define model, not using sequential
# first_input = Input(shape=(10, 24, 1))  # placed board
# first_dense = Conv2D(240, 4, use_bias=True)(first_input)
# first_dense = MaxPooling2D()(first_dense)
# first_dense = Dense(400, )(first_dense)
# first_dense = Flatten()(first_dense)
#
# second_input = Input(shape=(4, 4, 1))  # current piece
# second_dense = Conv2D(16, 2, use_bias=True)(second_input)
# second_dense = MaxPooling2D()(second_dense)
# second_dense = Dense(100, )(second_dense)
# second_dense = Flatten()(second_dense)
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

# load model
dir_str = "tetris_dqn_training/tetris_dqn_models"
dir_files = os.listdir(dir_str)
model = keras.models.load_model(dir_str + "/" + dir_files[-1])
model.summary()

epoch_total = 500
use_model_prediction = False

reward_list, inputs_list, action_taken_list = [], [], []
epoch = 0
time_start = time.time()
game_tick_index_list, lines_cleared_list = [], []
continue_train = True
while continue_train:
    # sort out inputs
    game_state = game.get_state()
    onedim_inputs = [game_state[1], game_state[2], game_state[3], game_state[5], game_state[6]]

    # store the inputs
    inputs_list.append([game_state[0], game_state[4], onedim_inputs])

    if use_model_prediction:
        # make a prediction, reshape to add batch size of 1
        action_proba = model.predict([np.array(game_state[0]).reshape((1, 10, 24, 1)),
                                      np.array(game_state[4]).reshape((1, 4, 4, 1)),
                                      np.array(onedim_inputs).reshape(1, 5)])

        # store the action
        action_taken_list.append(action_proba[0])

        # do the highest value action
        action_space[int(np.argmax(action_proba))]()
    else:
        # randomly select an action
        action_to_take = np.random.randint(len(action_space))
        # store the randomly selected action
        action_proba = np.zeros(len(action_space))
        action_proba[action_to_take] = 1
        action_taken_list.append(action_proba)

        # do the randomly selected action
        action_space[action_to_take]()

    # tick the game
    game.game_tick()

    # store the reward for training
    reward_list.append(game.lines_cleared - sum(reward_list))
    # reward_list.append(game.game_tick_index)
    # reward_list.append(game.game_tick_index * game.lines_cleared)
    # reward_list.append(game.game_tick_index ** game.lines_cleared)

    # check if game is over
    if not game.game_live:
        # train the model

        # to speed up, perhaps only fit at the end of epochs with lines_cleared > 0
        if game.lines_cleared > 0:
            # split inputs out again
            input0, input1, input2 = [], [], []
            for entry in inputs_list:
                input0.append(np.array(entry[0]).reshape((10, 24, 1)))
                input1.append(np.array(entry[1]).reshape(4, 4, 1))
                input2.append(np.array(entry[2]).reshape(5))

            # convert action list to have full confidence in chosen action
            action_taken_list = np.array(action_taken_list)
            action_taken_list_abs = np.zeros_like(action_taken_list)
            action_taken_list[np.argmax(action_taken_list)] = 1
            print(action_taken_list_abs)

            # fit the model
            model.fit([input0, input1, input2], action_taken_list_abs, sample_weight=np.array(reward_list), verbose=1)

        # reset the training data lists
        reward_list, inputs_list, action_taken_list = [], [], []

        # log progress
        epoch += 1
        print("Epoch: {}, GameTicks: {}, LinesCleared: {}, EstTimeRemaining(s): {}".format(epoch, game.game_tick_index, game.lines_cleared, (((time.time() - time_start) / (1 - ((epoch_total - epoch) / epoch_total)))) - (time.time() - time_start)))
        # print(game.placed_board)
        game_tick_index_list.append(game.game_tick_index)
        lines_cleared_list.append(game.lines_cleared)

        # reset the game
        game.game_reset()

        # finish training if epoch limit is reached
        if epoch == epoch_total:
            continue_train = False


print("---------")
print("ended")

print(game_tick_index_list)
print(lines_cleared_list)

# save model and training data
files_list = os.listdir("tetris_dqn_training/tetris_dqn_models")
files_list.sort()

if len(files_list) == 0:
    epoch_start = 0
    file_index = 0
else:
    file_index = int(files_list[-1].split("_")[0]) + 1
    epoch_start = int(files_list[-1].split("_")[-1].split(".h5")[0])

epoch_end = epoch_start + epoch
model.save("tetris_dqn_training/tetris_dqn_models/{}_tetris_dqn_model_{}_{}.h5".format(file_index, epoch_start, epoch_end))
pd.DataFrame([game_tick_index_list, lines_cleared_list]).to_csv("tetris_dqn_training/tetris_dqn_progress/{}_tetris_dqn_progress_{}_{}.csv".format(file_index, epoch_start, epoch_end), index=False)

