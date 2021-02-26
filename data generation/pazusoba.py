
from random import choice, randint

BOARD_INFO = {
    20: [5, 4],
    30: [6, 5],
    42: [7, 6]
}

class Location:
    """
    A wrapper for index to easily convert between index and location
    """

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
        if x >= 0 and x < self.get_row() and y >= 0 and y < self.get_column():
            return Location(self._convert_to_index((x, y)), self.board_size)
        return None

    def _get_location(self):
        column = self.get_column()
        # 11 / 5 = 2
        first = int(self.index / column)
        # 11 - 1 * 6 = 5
        second = self.index % column
        return [first, second]

    def _convert_to_index(self, location):
        (first, second) = location
        # 1 * 6 + 5 = 11
        return first * self.get_column() + second

    def get_row(self):
        """
        row is from left to right, usually 5
        """
        return BOARD_INFO[self.board_size][1]

    def get_column(self):
        """
        column is from top to bottom, usually 6
        """
        return BOARD_INFO[self.board_size][0]

class Pazusoba:
    """
    A basic port of pazusoba specialised in looking certain steps ahead
    """

    OUTPUT_TABLE = ["", "R", "B", "G", "L", "D", "H", "J", "P", "", "", "", ""]

    count = 0
    board_size = 0
    number = 0
    min_erase = 3

    def __init__(self, board_size, count, number):
        self.board_size = board_size
        self.count = count
        self.number = number

    def generate_new_data(self):
        """
        generate a new board and look ten steps ahead
        """

        # with open("data/data.csv", "a") as csv:
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
                best_score, best_board = self._look_ahead(orb_list, prev_location, curr_location)
                print(best_score, self._pretty_board(best_board))
                csv.write("{},{},{},{}\n".format(new_board, prev_location.get_index(), curr_location.get_index(), best_score))

    def _convert_board_to_list(self, board):
        return [int(x) for x in board.replace(" ", "").split(",")]

    def _look_ahead(self, board, prev, curr, step=10):
        score = 0
        best_board = []

        if step < 0:
            # calculate the score of the board
            return self._get_score(board)

        # move around
        for i in range(0, 4):
            next_loc = curr.move(i)
            
            # prevent invalid moves and going backward
            if next_loc == None or next_loc.get_index() == prev.get_index():
                continue

            # swap board and go deeper
            new_board = self._swap(board, curr, next_loc)

            # get the best score
            new_score, new_board = self._look_ahead(new_board, curr, next_loc, step - 1)
            if new_score > score:
                score = new_score
                best_board = new_board

        return (score, best_board)

    def _get_score(self, board):
        """
        get the score of the curren board, accuracy is the top priority
        """

        board_2d = self._convert_to_2d(board)
        row, column = self._get_board_info(board_2d)
        score = 0

        # continue until no new combo found
        more_combo = True
        while more_combo:
            more_combo = False

            # start from bottom to top
            for i in range(row - 1, -1, -1):
                # from left to right
                for j in range(0, column):
                    curr_orb = board_2d[i][j]
                    
                    # ignore empty orbs
                    if curr_orb == 0:
                        continue

                    combo_list = []
                    self._erase_combo(board_2d, i, j, curr_orb, combo_list, {})
                    new_score = 1000 if len(combo_list) >= self.min_erase else 0
                    score += new_score

                    if new_score > 0:
                        more_combo = True

            if more_combo:
                more_combo = self._move_orbs_down(board_2d)
                # more point for moving the board down
                if more_combo:
                    score += 50

        return (score, board)

    def _erase_combo(self, board, x, y, orb, combo_list, visited):
        """
        flood fill, copied from pazusoba
        """
        if not self._valid_location(board, x, y):
            return

        curr_orb = board[x][y]
        if curr_orb != orb and not (x, y) in visited:
            return

        count = -1
        d_list = [0, 0, 0, 0]
        # just put 3 for now
        minConnection = 3
        row, column = self._get_board_info(board)

        for d in range(4):
            loop = row
            if d > 1:
                loop = column

            for i in range(1, loop):
                cx, cy = x, y
                if d == 0:
                    cy += i
                elif d == 1:
                    cy -= i
                elif d == 2:
                    cx += i
                elif d == 3:
                    cx -= i

                if not self._valid_location(board, cx, cy):
                    break

                if board[cx][cy] != orb and not (cx, cy) in visited:
                    break
                    
                d_list[d] += 1
                count += 1

        if count >= minConnection:
            start, end = 0, 2

            h_count = d_list[0] + d_list[1] + 1
            v_count = d_list[2] + d_list[3] + 1
            horizontal = h_count >= minConnection
            vertical = v_count >= minConnection

            if h_count == 3 and v_count == 3:
                horizontal = vertical = True
            
            if not horizontal:
                start = 1
            if not vertical:
                end = 1

            for d in range(start, end):
                start_count = -(d_list[d * 2 + 1])
                end_count = d_list[d * 2] + 1
                for i in range(start_count, end_count):
                    cx, cy = x, y
                    if d == 0:
                        cy += i
                    elif d == 1:
                        cx += i

                    loc = (cx, cy)
                    if not loc in visited:
                        board[x][y] = 0
                        combo_list.append(loc)
                        visited[loc] = 1
                    else:
                        visited[loc] = 2

            for d in range(start, end):
                start_count = -(d_list[d * 2 + 1])
                end_count = d_list[d * 2] + 1
                for i in range(start_count, end_count):
                    cx, cy = x, y
                    if d == 0:
                        cy += i
                    elif d == 1:
                        cx += i
                    
                    if (cx, cy) in visited and visited[(cx, cy)] < 2:
                        if d == 0:
                            self._erase_combo(board, cx + 1, cy, orb, combo_list, visited)
                            self._erase_combo(board, cx - 1, cy, orb, combo_list, visited)
                        else:
                            self._erase_combo(board, cx, cy + 1, orb, combo_list, visited)
                            self._erase_combo(board, cx, cy - 1, orb, combo_list, visited)

    def _has_same_orb(self, board, orb, x, y):
        if self._valid_location(board, x, y):
            return board[x][y] == orb
        return False

    def _valid_location(self, board, x, y):
        row, column = self._get_board_info(board)
        return x >= 0 and x < row and y >= 0 and y < column

    def _move_orbs_down(self, board):
        """
        move orbs down and check if anything changed, copied from pazusoba, moveOrbsDown()
        """

        # this was before I updated column and row, so here it should be reverted
        row, column = self._get_board_info(board)
        changed = False

        for j in range(column):
            orbs = []
            empty_count = 0

            # start checking from the bottom
            for i in range(row - 1, -1, -1):
                orb = board[i][j]
                if orb > 0:
                    orbs.append(orb)
                else:
                    empty_count += 1

            # check empty but not all empty
            if empty_count > 0 and empty_count < column:
                k, s = 0, len(orbs)
                for i in range(row - 1, -1, -1):
                    if k >= s:
                        board[i][j] = 0
                    else:
                        orb = orbs[k]
                        curr_orb = board[i][j]
                        board[i][j] = orb
                        if curr_orb != orb:
                            changed = True
                    i -= 1
                    k += 1

        return changed

    def _convert_to_2d(self, board):
        """
        convert a board to a 2d array
        """

        column, row = BOARD_INFO[self.board_size]
        board_2d = []
        for i in range(row):
            board_row = []
            for j in range(column):
                board_row.append(board[j + i * column])
            board_2d.append(board_row)
        return board_2d

    def _get_board_info(self, board):
        return (len(board), len(board[0]))

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
        for num in board:
            output += self.OUTPUT_TABLE[int(num)]
        return output

    def _print_with_process(self, message):
        print("--- Process {} ---\n{}\n--- END ---\n".format(self.number, message))
