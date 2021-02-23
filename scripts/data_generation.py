"""
Generate random boards
"""

from os import cpu_count
from random import choice, randint
from board_pretty_print import pretty_board
from multiprocessing import Process

# 30 for 6 x 5, 42 for 7 x 6
board = 30

# seperate tasks to all cpus
cpu_count = cpu_count()
count = int(50000 / cpu_count)

def writeToFile(number):
    with open("temp.txt", "a") as temp:
        for i in range(count):
            temp.write("{} - {}\n".format(number, i))
        temp.close()

if __name__ == '__main__':
    processes = []
    for i in range(cpu_count):
        print("Process {}".format(i))
        processes.append(Process(target=writeToFile, args=(i,)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

# with open("/data/data.csv", "a") as csv:
#     for i in range(0, count):
#         new_board = ""
#         ORBS = list(range(1, 7))

#         # 50% chance to get a board with less orbs
#         if randint(0, 1) == 0:
#             number_of_orbs = randint(2, 5)
#             while len(ORBS) > number_of_orbs:
#                 ORBS.remove(choice(ORBS))

#         for j in range(0, board):
#             orb = choice(ORBS)
#             new_board += "{}{}".format(orb, "," if j < board - 1 else "")
#         print(pretty_board(new_board))
#         # csv.write(new_board + "\n")
#     csv.close()
