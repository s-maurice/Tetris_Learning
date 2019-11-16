import random
from keras.layers import Dense
from keras.models import Sequential

from TetrisGame import TetrisGame

game = TetrisGame()
action_space = [lambda: game.move_rotate(1),
                lambda: game.move_horizontal(1),
                lambda: game.move_horizontal(-1),
                lambda: game.move_drop_hard()]

# define model
model = Sequential()
# add hidden layer
model.add(Dense(units=200, input_dim=(20, 20), activation='relu', kernel_initializer='glorot_uniform'))
# add output layer (4 possible actions)
model.add(Dense(units=4, activation='sigmoid', kernel_initializer='RandomNormal'))
# compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


for tick in range(500):
    # do an action
    random.choice(action_space)()
    # tick the game
    game.game_tick()
    if not game.game_live:
        print(tick)
        print(game.placed_board)
        game.game_reset()

