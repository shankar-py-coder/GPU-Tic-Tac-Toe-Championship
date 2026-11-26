
import numpy as np

class TicTacToe:

    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)

    def make_move(self, position, player):

        if position < 0 or position > 8:
            return False

        row = position // 3
        col = position % 3

        if self.board[row][col] == 0:
            self.board[row][col] = player
            return True

        return False

    def check_winner(self):

        lines = []

        lines.extend(self.board.tolist())
        lines.extend(self.board.T.tolist())

        lines.append([self.board[i][i] for i in range(3)])
        lines.append([self.board[i][2-i] for i in range(3)])

        for line in lines:
            if line[0] != 0 and line.count(line[0]) == 3:
                return line[0]

        if not np.any(self.board == 0):
            return -1

        return 0

    def display(self):

        symbols = {0: ".", 1: "X", 2: "O"}

        print("\n-------------")

        for row in self.board:
            print("|", end=" ")

            for cell in row:
                print(symbols[cell], end=" | ")

            print("\n-------------")
