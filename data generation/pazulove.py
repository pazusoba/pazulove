"""
Generate data for machine learning
"""

import random
from find_max_combo import findMaxCombo

ORBS = ["R", "B", "G", "L", "D", "H"]
EXTRA_ORBS = ["P", "J"]


class PazuLove:
    def __init__(self, size, step, process, count):
        self.size = size
        self.step = step
        # the current process number
        self.process = process
        # the number of data to generate
        self.count = count

    def generate_new_data(self):
        with open("../data/data{}_random.csv".format(self.step), "a") as csv:
            for i in range(self.count):
                output = ""
                board = ""
                for i in range(self.size):
                    orb = random.choice(ORBS)
                    board += orb
                    output += str(ORBS.index(orb)) + ","
                combo = findMaxCombo(board, self.step)
                output += str(combo) + "\n"
                csv.write(output)
