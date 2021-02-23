"""
A basic port of pazusoba specialised in looking certain steps ahead
"""

from random import choice, randint

class Pazusoba:
    OUTPUT_TABLE = ["", "R", "B", "G", "L", "D", "H", "J", "P", "", "", "", ""]\
    BOARD_INFO = [
        20: [5, 4],
        30: [6, 5],
        42: [7, 6]
    ]

    count = 0
    board_size = 0
    number = 0

    def __init__(self, board_size, count, number):
        self.board_size = board_size
        self.count = count
        self.number = number

    def generate_new_data(self):
        """
        generate a new board and look ten steps ahead
        """

        for i in range(0, self.count):
            new_board = ""
            orbs = list(range(1, 7))

            # 50% chance to get a board with less orbs
            if randint(0, 1) == 0:
                number_of_orbs = randint(2, 5)
                while len(orbs) > number_of_orbs:
                    orbs.remove(choice(orbs))

            for j in range(0, self.board_size):
                orb = choice(orbs)
                new_board += "{}{}".format(orb, "," if j < self.board_size - 1 else "")
            
            # pick random locations
            curr_location = randint(0, 29)
            prev_location = 0

            # 4% chance to be -1 which means this is the first move
            if randint(0, 99) < 4:
                prev_location = -1
            else:
                # introduce Location here to convert between index and loc?
                pass

            # debug only 
            self._convert_board_to_list(new_board)
            self._print_with_process("No.{} - {}\nPrev - {}, Curr - {}".format(i, self._pretty_board(new_board), prev_location, curr_location))

    def _convert_board_to_list(self, board):
        return [int(x) for x in board.replace(" ", "").split(",")]

    def _get_row(self):
        return self.BOARD_INFO[self.board_size][1]

    def _get_column(self):
        return self.BOARD_INFO[self.board_size][0]

    def _look_ahead(self, board, prev, curr, step=10):
        print(step)

    def _pretty_board(self, board):
        """
        convert board to the format used by https://pad.dawnglare.com/
        """

        output = ""
        for num in self._convert_board_to_list(board):
            output += self.OUTPUT_TABLE[int(num)]
        return output

    def _print_with_process(self, message):
        print("--- Process {} ---\n{}\n--- END ---\n".format(self.number, message))
