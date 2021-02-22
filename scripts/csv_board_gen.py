"""
Generate random boards
"""

from random import randint

# 30 for 6 x 5, 42 for 7 x 6
board = 30
count = 30

for i in range(0, count):
    for j in range(0, count):
        # from fire orb to unknown
        orb = randint(1, 6)
        print("{}{} ".format(orb, "," if j < board - 1 else ""), end='')
    print()
