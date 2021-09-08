import sys

ORBS = ["R", "B", "G", "L", "D", "H", "J", "P"]

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # ignore the score
        csv_row = sys.argv[1].strip()[:-1]

        board = ""
        for num in csv_row.split(","):
            if num != '':
                board += ORBS[int(num)]

        print(board)
