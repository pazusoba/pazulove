"""
Generate random boards
"""

from random import choice, randint
from csv_board_convert import convert_board

# 30 for 6 x 5, 42 for 7 x 6
board = 30
count = 700

with open("../data/data.csv", "a") as csv:
    for i in range(0, count):
        new_board = ""
        ORBS = list(range(1, 7))

        # 50% chance to get a board with less orbs
        if randint(0, 1) == 0:
            number_of_orbs = randint(2, 5)
            while len(ORBS) > number_of_orbs:
                ORBS.remove(choice(ORBS))

        for j in range(0, board):
            orb = choice(ORBS)
            new_board += "{}{}".format(orb, ", " if j < board - 1 else "")
        # print(convert_board(new_board))
        csv.write(new_board + "\n")
    csv.close()
