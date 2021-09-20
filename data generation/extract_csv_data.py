"""
Extract data from csv file with score and count
"""

import random

score = 9
count = 100
csv_file_name = 'data8_normal.csv'

if __name__ == '__main__':
    with open('../data/{}'.format(csv_file_name), 'r') as csv:
        items = []
        for line in csv.readlines():
            parts = line.split(',')
            if parts[-1].strip() == str(score):
                items.append(line.strip())

        csv.close()

        if len(items) > count:
            items = random.sample(items, count)
        for item in items:
            print(item)
        print("total {} item(s)".format(len(items)))
