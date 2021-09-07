"""
Call methods exported in the shared library
"""
from ctypes import *
from typing import List
import os

LIBRARY = "libpazulove.so"
if not os.path.exists(LIBRARY):
    print("{} is not found at current directory".format(LIBRARY))

libpazusoba = CDLL(LIBRARY, winmode=0)
libpazusoba.findMaxCombo.restype = c_int
libpazusoba.findMaxCombo.argtypes = (c_char_p, c_uint)


def findMaxCombo(board: str, step: int) -> int:
    # convert to c string
    c_board = c_char_p(board.encode('ascii'))
    return libpazusoba.findMaxCombo(c_board, step)

if __name__ == '__main__':
    combo = findMaxCombo("RHLBDGPRHDRJPJRHHJGRDRHLGLPHBB", 10)
    print("Max combo is {}\n".format(combo))
