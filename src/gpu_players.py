
import ctypes
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

player1_lib = ctypes.CDLL(
    os.path.join(BASE_DIR, "player1.so")
)

player2_lib = ctypes.CDLL(
    os.path.join(BASE_DIR, "player2.so")
)

INT_POINTER = ctypes.POINTER(ctypes.c_int)

player1_lib.get_player1_move.argtypes = [
    INT_POINTER, INT_POINTER
]
player1_lib.get_player1_move.restype = None

player2_lib.get_player2_move.argtypes = [
    INT_POINTER, INT_POINTER
]
player2_lib.get_player2_move.restype = None


def get_player1_move(board):

    board_array = np.ascontiguousarray(
        board, dtype=np.int32
    ).reshape(9)

    move = ctypes.c_int(-1)

    player1_lib.get_player1_move(
        board_array.ctypes.data_as(INT_POINTER),
        ctypes.byref(move)
    )

    return move.value


def get_player2_move(board):

    board_array = np.ascontiguousarray(
        board, dtype=np.int32
    ).reshape(9)

    move = ctypes.c_int(-1)

    player2_lib.get_player2_move(
        board_array.ctypes.data_as(INT_POINTER),
        ctypes.byref(move)
    )

    return move.value


print("Both GPU competitors connected successfully!")
