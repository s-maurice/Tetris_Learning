import random

from keras import Input, Model
from keras.layers import Dense, Embedding, concatenate, Reshape
from keras.models import Sequential
import numpy as np
from tensorflow import keras

from TetrisGame import TetrisGame

game = TetrisGame()
action_space = [lambda: game.move_rotate(1),
                lambda: game.move_horizontal(1),
                lambda: game.move_horizontal(-1),
                lambda: game.move_drop_hard()]

# define model, not using sequential
first_input = Input(shape=(10, 24))  # placed board
first_dense = Dense(100, )(first_input)
first_dense = Reshape((1000,))(first_dense)


second_input = Input(shape=(4, 4))  # current piece
second_dense = Dense(250, )(second_input)
second_dense = Reshape((1000,))(second_dense)

merge_one = concatenate([first_dense, second_dense])

third_input = Input(shape=(5, ))  # single dim values
merge_two = concatenate([merge_one, third_input])

output = Dense(4, input_shape=(2005, ))(merge_two)

model = Model(inputs=[first_input, second_input, third_input], outputs=output)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()


reward_list, inputs_list, action_taken_list = [], [], []
for tick in range(500):
    # get observation
    # print(game.get_state())

    # do an action
    # [print(np.array(item).shape) for item in game.get_state()]

    # sort out inputs
    game_state = game.get_state()
    onedim_inputs = [game_state[1], game_state[2], game_state[3], game_state[5], game_state[6]]
    inputs = [np.array(game_state[0]).reshape((1, 10, 24)),
              np.array(game_state[4]).reshape((1, 4, 4)),
              np.array(onedim_inputs).reshape(1, 5)]

    # store the inputs
    inputs_list.append(inputs)

    # perform a prediction
    action_proba = model.predict(inputs)

    # store the action
    # action_taken_list.append(np.argmax(action_proba))
    action_taken_list.append(action_proba)

    # do the highest values
    action_space[np.argmax(action_proba)]()

    # tick the game
    game.game_tick()

    # store the reward for training
    reward_list.append(game.game_tick_index)



    if not game.game_live:
        # train the model
        model.fit(inputs, action_taken_list, sample_weight=game.game_tick_index)

        # reset the game if it's over
        print(game.placed_board)
        game.game_reset()

print(reward_list)
# print(action_taken_list)
# print(inputs_list)
print(max(reward_list))

print("---------")
# print(np.array(inputs_list[0]))

# train model with rewards and actions
model.fit(inputs_list, action_taken_list, sample_weight=reward_list)
model.save("model")

