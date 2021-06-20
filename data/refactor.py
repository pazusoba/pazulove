'''
Remove previous and current, simplify score to combo number only.
Start from 0 and up to 5
'''

import sys
import os

file_path = sys.argv[1]

if not file_path.endswith('csv'):
    exit("Not a csv file")
if not os.path.exists(file_path):
    exit("File doesn't exists")

with open(file_path, "r") as csv_file:
    with open(file_path + '_new', 'w') as new_csv_file:
        for line in csv_file.readlines():
            if line.startswith('orb0,'):
                new_csv_file.write(line)
            else:
                # seperate by , and remove next prev, also simplify the score
                components = line.split(',')

                # -3 items, they are the actual boards
                board = components[:-3]
                for orb in board:
                    orb_value = int(orb)
                    new_csv_file.write(str(orb_value - 1) + ',')

                score = int(components[-1])
                combo = int(score / 1000)
                new_csv_file.write(str(combo) + '\n')
            