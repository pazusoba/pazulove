"""
Call methods exported in the shared library
"""
from ctypes import *
import os, sys
import time

LIBRARY = "libpazulove.so"
if not os.path.exists(LIBRARY):
    print("{} is not found at current directory".format(LIBRARY))

libpazusoba = CDLL(LIBRARY, winmode=0)
libpazusoba.findMaxCombo.restype = c_int
libpazusoba.findMaxCombo.argtypes = (c_char_p, c_uint)


def findMaxCombo(board: str, step: int) -> int:
    # convert to c string
    return libpazusoba.findMaxCombo(board.encode('utf-8'), step)

if __name__ == '__main__':
    start = time.time()
    # "RHLBDGPRHDRJPJRHHJGRDRHLGLPHBB"
    if len(sys.argv) > 1:
        board = sys.argv[1]
        step = 10
        if len(sys.argv) > 2:
            step = int(sys.argv[2])

        combo = findMaxCombo(board, step)
        print("{} - {}".format(board, combo))
    print(time.time() - start)
