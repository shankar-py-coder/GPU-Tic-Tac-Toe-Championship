
import sys
import threading
import numpy as np
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "/content/GPU_Tic_Tac_Toe/src")

from game import TicTacToe
from gpu_players import get_player1_move, get_player2_move

# Shared lock: only one CUDA operation at a time
gpu_lock = threading.Lock()


def player1_worker(board):
    with gpu_lock:
        return get_player1_move(board)


def player2_worker(board):
    with gpu_lock:
        return get_player2_move(board)


def play_game():

    game = TicTacToe()

    # Dedicated thread for each GPU competitor
    player1_thread = ThreadPoolExecutor(
        max_workers=1,
        thread_name_prefix="GPU_Player_1"
    )

    player2_thread = ThreadPoolExecutor(
        max_workers=1,
        thread_name_prefix="GPU_Player_2"
    )

    print("\n================================")
    print(" GPU TIC-TAC-TOE CHAMPIONSHIP")
    print("================================")
    print("Player 1: Dedicated GPU worker thread")
    print("Player 2: Dedicated GPU worker thread")

    try:
        for turn in range(9):

            board_copy = game.board.copy()

            if turn % 2 == 0:
                future = player1_thread.submit(
                    player1_worker, board_copy
                )
                player = 1
                name = "GPU Player 1 (X)"
            else:
                future = player2_thread.submit(
                    player2_worker, board_copy
                )
                player = 2
                name = "GPU Player 2 (O)"

            move = future.result()

            if not game.make_move(move, player):
                raise RuntimeError("Invalid move received!")

            print(f"\nTurn {turn + 1}: {name}")
            print("Selected position:", move)

            game.display()

            winner = game.check_winner()

            if winner == 1:
                print("\nGPU PLAYER 1 WINS!")
                break
            elif winner == 2:
                print("\nGPU PLAYER 2 WINS!")
                break
            elif winner == -1:
                print("\nMATCH DRAW!")
                break

    finally:
        player1_thread.shutdown(wait=True)
        player2_thread.shutdown(wait=True)

    print("\nBoth competitor threads completed.")


if __name__ == "__main__":
    play_game()
