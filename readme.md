Single-Player Tetris:
allow for ml training for optimal play and development of strategies
various scoring systems - combos and chain bonuses
implementation of foresight and upcoming tetris blocks
training with various amounts of information/synthetics

Multi-Player Tetris Battle:
allow for training of attacking and defending battle strategies
training against self
warm starting against cold starting of training - with or without prior knowledge of Single-Player play
training with varying amounts of opponent information/synthetics
playing against heuristic opponent

Training Strategies:
recording human-player inputs and features and warm starting model
randomly selecting action from action space at the beginning to increase training speed
randomly mutate the model by randomly choosing to use the model decision or a random decision

Notes - Features to be added:
increase action space to contain all possible actions
add feature for locations to clear top line - 1x10 slice of gap locations (done)
add feature for distance and rotation to drop point to clear line
add feature for the complete board when the piece is dropped right now
add feature for width and height of current piece (done)
add feature for the number of horizontal and vertical blocks the current piece and saved piece take up - to help determine rotation
convert draw_board into class, allowing for func calling to draw any board - used to illustrate boards during training (done)
change reward function to reward keeping the board height low - so it tries to avoid stacking up

alternative methodology - give all the locations of the possible placements and have the model decide between them