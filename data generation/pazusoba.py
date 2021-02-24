
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
        move up, down, left or right one step. 4% chance to be -1 which means this is the first move
        """

        new_location = Location(-1, self.board_size)
        if randint(0, 99) < 4:
            return new_location
        else:
            d = list(range(0, 4))
            while len(d) > 0:
                pick = choice(d)
                d.remove(pick)

                new_location = self.move(pick)
                if new_location != None:
                    break
            return new_location

    def get_index(self):
        return self.index

    def move(self, number):
        """
        move based on the number
        0 - up
        1 - down
        2 - left
        3 - right
        """

        (x, y) = self.location
        if number == 0:
            x -= 1
        elif number == 1:
            x += 1
        elif number == 2:
            y -= 1
        elif number == 3:
            y += 1

        # check if the new location is valid
        if x >= 0 and x < self._get_row() and y >= 0 and y < self._get_column():
            return Location(self._convert_to_index((x, y)), self.board_size)
        return None

    def _get_location(self):
        column = self._get_column()
        # 11 / 5 = 2
        first = int(self.index / column)
        # 11 - 1 * 6 = 5
        second = self.index % column
        return [first, second]

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
    number_of_recursion = 0

    def __init__(self, board_size, count, number):
        self.board_size = board_size
        self.count = count
        self.number = number

    def generate_new_data(self):
        """
        generate a new board and look ten steps ahead
        """

        with open("temp.txt", "a") as csv:
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
                prev_location = curr_location.get_random_previous_location()
                
                orb_list = self._convert_board_to_list(new_board)
                # self._print_with_process("No.{} - {}\nPrev - {}, Curr - {}".format(i, self._pretty_board(new_board), prev_location.get_index(), curr_location.get_index()))
                best_score = self._look_ahead(orb_list, prev_location, curr_location)

                csv.write("{},{},{},{}\n".format(new_board, prev_location.get_index(), curr_location.get_index(), best_score))
                self.number_of_recursion = 0

    def _convert_board_to_list(self, board):
        return [int(x) for x in board.replace(" ", "").split(",")]

    def _look_ahead(self, board, prev, curr, step=10):
        self.number_of_recursion += 1
        if step < 0:
            # we need to calculate the score
            return

        # move around
        for i in range(0, 4):
            next_loc = curr.move(i)
            
            # prevent invalid moves and going backward
            if next_loc == None or next_loc.get_index() == prev.get_index():
                continue

            # swap board and go deeper
            new_board = self._swap(board, curr, next_loc)
            self._look_ahead(new_board, curr, next_loc, step - 1)

    def _swap(self, board, first, second):
        # copy the board, swap two location
        new_board = board[:]
        new_board[first.get_index()], new_board[second.get_index()] = new_board[second.get_index()], new_board[first.get_index()]
        return new_board

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
