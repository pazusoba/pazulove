
from random import choice, randint

class Location:
    """
    A wrapper for index to easily convert between index and location
    """

    BOARD_INFO = {
        20: [5, 4],
        30: [6, 5],
        42: [7, 6]
    }

    index = 0
    board_size = 0
    location = (0, 0)

    def __init__(self, index, board_size):
        self.index = index
        self.board_size = board_size
        self.location = self._get_location()

    def get_random_previous_location(self):
        """
        move up, down, left or right one step
        """
        return Location(0, self.board_size)

    def index(self):
        return self._convert_to_index(self.index)

    def _get_location(self):
        # 11 / 5 - 1 = 1
        first = int(self.index / self._get_row()) - 1
        # 11 - 1 * 6 = 5
        second = self.index - first * self._get_column()
        return (first, second)

    def _convert_to_index(self, location):
        (first, second) = location
        # 1 * 6 + 5 = 11
        return first * self._get_column() + second

    def _get_row(self):
        return self.BOARD_INFO[self.board_size][1]

    def _get_column(self):
        return self.BOARD_INFO[self.board_size][0]

class Pazusoba:
    """
    A basic port of pazusoba specialised in looking certain steps ahead
    """

    OUTPUT_TABLE = ["", "R", "B", "G", "L", "D", "H", "J", "P", "", "", "", ""]\

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
            curr_location = Location(randint(0, self.board_size - 1), self.board_size)
            # 4% chance to be -1 which means this is the first move
            if randint(0, 99) < 4:
                prev_location = Location(-1, self.board_size)
            else:
                prev_location = curr_location.get_random_previous_location()

            print(prev_location.index())
            # debug only 
            self._convert_board_to_list(new_board)
            self._print_with_process("No.{} - {}\nPrev - {}, Curr - {}".format(i, self._pretty_board(new_board), prev_location, curr_location))

    def _convert_board_to_list(self, board):
        return [int(x) for x in board.replace(" ", "").split(",")]

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
