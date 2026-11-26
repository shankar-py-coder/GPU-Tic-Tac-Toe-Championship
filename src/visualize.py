
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

sys.path.insert(0, os.path.dirname(__file__))

from game import TicTacToe
from gpu_players import get_player1_move, get_player2_move

game = TicTacToe()

frames = []
messages = []

frames.append(game.board.copy())
messages.append("GPU Tic-Tac-Toe Championship")

for turn in range(9):

    if turn % 2 == 0:
        player = 1
        move = get_player1_move(game.board)
        name = "GPU Player 1 (X)"
    else:
        player = 2
        move = get_player2_move(game.board)
        name = "GPU Player 2 (O)"

    if not game.make_move(move, player):
        raise RuntimeError("Invalid GPU move detected!")

    frames.append(game.board.copy())
    messages.append(f"{name} - Turn {turn + 1}")

    winner = game.check_winner()

    if winner == 1:
        result = "GPU PLAYER 1 WINS!"
        break
    elif winner == 2:
        result = "GPU PLAYER 2 WINS!"
        break
    elif winner == -1:
        result = "MATCH DRAW!"
        break

fig, ax = plt.subplots(figsize=(7, 7))

def update(frame):

    ax.clear()
    ax.set_xlim(0, 3)
    ax.set_ylim(3, 0)
    ax.set_aspect("equal")

    ax.set_xticks([])
    ax.set_yticks([])

    for i in range(4):
        ax.plot([i, i], [0, 3], color="#34495E", linewidth=3)
        ax.plot([0, 3], [i, i], color="#34495E", linewidth=3)

    board = frames[frame]

    for r in range(3):
        for c in range(3):

            if board[r][c] == 1:
                ax.text(
                    c + 0.5, r + 0.5, "X",
                    fontsize=55,
                    fontweight="bold",
                    color="#2980B9",
                    ha="center",
                    va="center"
                )

            elif board[r][c] == 2:
                ax.text(
                    c + 0.5, r + 0.5, "O",
                    fontsize=55,
                    fontweight="bold",
                    color="#E67E22",
                    ha="center",
                    va="center"
                )

    if frame == len(frames) - 1:
        title = result
    else:
        title = messages[frame]

    ax.set_title(
        title,
        fontsize=17,
        fontweight="bold",
        pad=20
    )

    ax.set_facecolor("#F4F6F7")
    fig.patch.set_facecolor("#F4F6F7")


animation = FuncAnimation(
    fig,
    update,
    frames=len(frames),
    interval=900,
    repeat=False
)

output = "/content/GPU_Tic_Tac_Toe/results/game_animation.gif"

animation.save(
    output,
    writer=PillowWriter(fps=1.2)
)

plt.close(fig)

print("Game visualization created successfully!")
print("Final result:", result)
print("Saved at:", output)
