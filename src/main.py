
import sys
import numpy as np

from game import TicTacToe
from gpu_players import get_player1_move, get_player2_move


def play_game():

    game = TicTacToe()

    print("\n================================")
    print("     GPU TIC-TAC-TOE CHAMPIONSHIP")
    print("================================")

    print("\nGPU Player 1: X")
    print("GPU Player 2: O")

    move_history = []

    for turn in range(9):

        if turn % 2 == 0:
            player = 1
            symbol = "X"
            move = get_player1_move(game.board)
            player_name = "GPU Player 1"
        else:
            player = 2
            symbol = "O"
            move = get_player2_move(game.board)
            player_name = "GPU Player 2"

        if not game.make_move(move, player):
            print("Invalid move detected!")
            return

        move_history.append({
            "turn": turn + 1,
            "player": player_name,
            "symbol": symbol,
            "position": move
        })

        print(f"\nTurn {turn + 1}: {player_name} played {symbol}")
        print(f"Selected position: {move}")

        game.display()

        winner = game.check_winner()

        if winner == 1:
            print("\n🏆 GPU PLAYER 1 (X) WINS!")
            break

        elif winner == 2:
            print("\n🏆 GPU PLAYER 2 (O) WINS!")
            break

        elif winner == -1:
            print("\n🤝 MATCH DRAW!")
            break

    print("\n========== MATCH SUMMARY ==========")

    for item in move_history:
        print(
            f"Turn {item['turn']}: "
            f"{item['player']} - "
            f"Position {item['position']}"
        )

    print("\n===================================")


if __name__ == "__main__":
    play_game()
