"""
Convert board data from csv to readable format
"""

import sys

OUTPUT_TABLE = ["", "R", "B", "G", "L", "D", "H", "J", "P", "", "", "", ""]

board = "5, 3, 5, 4, 6, 4, 6, 5, 6, 3, 3, 5, 2, 5, 4, 5, 3, 5, 6, 4, 2, 4, 2, 2, 1, 4, 1, 2, 8, 7"
if len(sys.argv) > 1:
    board = sys.argv[1] if "," in sys.argv[1] else board

for num in board.replace(" ", "").split(","):
    if num.isnumeric():
        print(OUTPUT_TABLE[int(num)], end="")
    else:
        exit("Input '{}' wasn't valid".format(board))
