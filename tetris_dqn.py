import random

from TetrisGame import TetrisGame

game = TetrisGame()
action_space = [lambda: game.move_rotate(1),
                lambda: game.move_horizontal(1),
                lambda: game.move_horizontal(-1),
                lambda: game.move_drop_hard()]

for tick in range(500):
    # do an action
    random.choice(action_space)()
    # tick the game
    game.game_tick()

    if not game.game_live:
        print(tick)
        print(game.placed_board)
        game.game_reset()

