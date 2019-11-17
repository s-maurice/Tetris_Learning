import time

from keras import Input, Model
from keras.layers import Dense, Embedding, concatenate, Reshape
from keras.models import Sequential
import numpy as np
import matplotlib.pyplot as plt

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

total_epochs = 200

reward_list, inputs_list, action_taken_list = [], [], []
epoch = 0
time_start = time.time()
game_tick_index_list, lines_cleared_list = [], []
continue_train = True
while continue_train:
    # get observation
    # print(game.get_state())

    # do an action
    # [print(np.array(item).shape) for item in game.get_state()]

    # sort out inputs
    game_state = game.get_state()
    onedim_inputs = [game_state[1], game_state[2], game_state[3], game_state[5], game_state[6]]

    # store the inputs
    inputs_list.append([game_state[0], game_state[4], onedim_inputs])

    # perform a prediction, reshape to add batch size of 1
    action_proba = model.predict([np.array(game_state[0]).reshape((1, 10, 24)),
                                  np.array(game_state[4]).reshape((1, 4, 4)),
                                  np.array(onedim_inputs).reshape(1, 5)])

    # store the action
    # action_taken_list.append(np.argmax(action_proba))
    action_taken_list.append(action_proba[0])

    # do the highest values
    action_space[np.argmax(action_proba)]()

    # tick the game
    game.game_tick()

    # store the reward for training
    # reward_list.append(game.game_tick_index)
    # reward_list.append(game.game_tick_index * game.lines_cleared)
    reward_list.append(game.game_tick_index ** game.lines_cleared)

    # check if game is over
    if not game.game_live:
        # train the model
        # split inputs out again
        input0, input1, input2 = [], [], []
        for entry in inputs_list:
            input0.append(entry[0])
            input1.append(entry[1])
            input2.append(entry[2])

        model.fit([input0, input1, input2], np.array(action_taken_list), sample_weight=np.array(reward_list), verbose=1)

        # reset the training data lists
        reward_list, inputs_list, action_taken_list = [], [], []

        epoch += 1

        # log progress
        print("Epoch: {}, GameTicks: {}, LinesCleared: {}, EstTimeRemaining(s): {}".format(epoch, game.game_tick_index, game.lines_cleared, (((time.time() - time_start) / (1 - ((total_epochs - epoch) / total_epochs)))) - (time.time() - time_start)))
        # print(game.placed_board)
        if epoch == total_epochs:
            continue_train = False
        game_tick_index_list.append(game.game_tick_index)
        lines_cleared_list.append(game.lines_cleared)

        # reset the game
        game.game_reset()


print("---------")
print("ended")

print(game_tick_index_list)
print(lines_cleared_list)

# Plot the training progress
fig, ax1 = plt.subplots()
ax1.set_ylabel('Game Ticks at Game Over', color="r")
ax1.tick_params(axis='y', labelcolor="r")
line1 = ax1.plot(game_tick_index_list, label="Game Ticks Survived", color="r")
ax1.set_xlabel('Game Number')

ax2 = ax1.twinx()
ax2.set_ylabel('Lines Cleared at Game Over', color="b")
ax2.tick_params(axis='y', labelcolor="b")
line2 = ax2.plot(lines_cleared_list, label="Lines Cleared", color="b")

lines = line1+line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper right")

fig.tight_layout()
plt.show()

# save model
model.save("model.h5")

