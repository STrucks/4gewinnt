import numpy as np


class Board:

    WIDTH, HEIGHT = 10, 7

    def __init__(self, _width_, _height_):
        self.WIDTH = _width_
        self.HEIGHT = _height_
        self.field = np.zeros(shape=(self.HEIGHT, self.WIDTH))

    def to_string(self):
        result = ""
        for index_y, row in enumerate(self.field):
            sb = str(index_y)
            for index_x, value in enumerate(row):
                if value == 0:
                    sb += "."
                elif value == 1:
                    sb += "o"
                else:
                    sb += "x"
            result += sb + "\n"
        sb = " "
        if self.WIDTH < 10:
            sb += "".join(range(self.WIDTH))
        elif self.WIDTH < 100:
            for i in range(self.WIDTH):
                if i < 10:
                    sb += " "
                else:
                    sb += str(i)[0]
            sb += "\n "
            for i in range(self.WIDTH):
                if i < 10:
                    sb += str(i)[0]
                else:
                    sb += str(i)[1]

        result += sb
        return result

    def possible_positions(self):
        positions = []
        for x in range(self.WIDTH):
            for y in reversed(range(self.HEIGHT)):
                if self.field[y, x] == 0:
                    positions.append((x, y))
                    break
        return positions

    def move(self, x, y, player):
        if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:

            if self.field[y, x] == 0:
                if y + 1 < self.HEIGHT:
                    if self.field[y+1, x] != 0:
                        self.field[y, x] = player
                        return True
                    else:
                        return False
                else:
                    self.field[y, x] = player
                    return True
            else:
                return False
        else:
            return False

    def is_winning_state(self):
        # check horizontally:
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH-4):
                value = self.field[y,x]
                if value == 0:
                    continue
                conv = [1]
                for i in range(1, 4):
                    if self.field[y, x+i] == value:
                        conv.append(1)
                if sum(conv) == 4:
                    print("winning at", x, y)
                    return True, value
        return False, value





if __name__ == '__main__':
    WIDTH, HEIGHT = 20, 7
    board = Board(WIDTH, HEIGHT)
    players = [1,2]
    player_index = 0
    for i in range(100):
        possible = board.possible_positions()
        move = possible[np.random.randint(0, len(possible))]
        valid = board.move(move[0],move[1], players[player_index])
        if not valid:
            print("move", move, "is not valid")
            break
        win, who = board.is_winning_state()
        if win:
            break
        player_index += 1
        player_index %= 2
        print(board.to_string())
    print(board.to_string())
    print(board.possible_positions())
