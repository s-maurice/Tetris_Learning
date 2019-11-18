import matplotlib.pyplot as plt
import os
import pandas as pd

dir_str = "tetris_dqn_training/tetris_dqn_progress"
dir_file_list = os.listdir(dir_str)
dir_file_list.sort()

df_list = []
for file_str in dir_file_list:
    df_list.append(pd.read_csv(dir_str + "/" + file_str, header=None, index_col=False).transpose().drop(0, axis=1))

data = pd.concat(df_list, ignore_index=True)
print(data)

# Plot the training progress
fig, ax1 = plt.subplots()
ax1.set_ylabel('Game Ticks at Game Over', color="r")
ax1.tick_params(axis='y', labelcolor="r")
line1 = ax1.plot(data[1], label="Game Ticks Survived", color="r")
ax1.set_xlabel('Game Number')

ax2 = ax1.twinx()
ax2.set_ylabel('Lines Cleared at Game Over', color="b")
ax2.tick_params(axis='y', labelcolor="b")
line2 = ax2.plot(data[2], label="Lines Cleared", color="b")

lines = line1+line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper right")

fig.tight_layout()
plt.show()
