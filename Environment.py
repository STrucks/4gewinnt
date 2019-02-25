import numpy as np


class Board:

    WIDTH, HEIGHT = 10, 7

    def __init__(self, _width_, _height_, max_steps):
        self.WIDTH = _width_
        self.HEIGHT = _height_
        self.field = np.zeros(shape=(self.HEIGHT, self.WIDTH))
        self.max_steps = max_steps
        self.steps = 0

    def to_string(self):
        result = ""
        for index_y, row in enumerate(self.field):
            sb = str(index_y)
            for index_x, value in enumerate(row):
                if value == 0:
                    sb += " ."
                elif value == 1:
                    sb += " o"
                else:
                    sb += " x"
            result += sb + "\n"
        sb = "  "
        if self.WIDTH < 10:
            sb += " ".join([str(x) for x in range(self.WIDTH)])
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

    def is_winning_state(self, out_print=False):
        # check horizontally:
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH - 3):
                value = self.field[y, x]
                if value == 0:
                    continue
                conv = [1]
                for i in range(1, 4):
                    if self.field[y, x + i] == value:
                        conv.append(1)
                if sum(conv) == 4:
                    if out_print:
                        print("winning at", x, y, "to", x+3, y)
                    return True, value

        # check vertically:
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT - 3):
                value = self.field[y, x]
                if value == 0:
                    continue
                conv = [1]
                for i in range(1, 4):
                    if self.field[y + i, x] == value:
                        conv.append(1)
                if sum(conv) == 4:
                    if out_print:
                        print("winning at", x, y, "to", x, y+3)
                    return True, value
        # check diagonally:
        for x in range(self.WIDTH - 3):
            for y in range(self.HEIGHT - 3):
                value = self.field[y, x]
                if value == 0:
                    continue
                conv = [1]
                for i in range(1, 4):
                    if self.field[y + i, x + i] == value:
                        conv.append(1)
                if sum(conv) == 4:
                    if out_print:
                        print("winning at", x, y, "to", x + 3, y + 3)
                    return True, value
        for x in range(3, self.WIDTH):
            for y in range(self.HEIGHT - 3):
                value = self.field[y, x]
                if value == 0:
                    continue
                conv = [1]
                for i in range(1, 4):
                    if self.field[y + i, x - i] == value:
                        conv.append(1)
                if sum(conv) == 4:
                    if out_print:
                        print("winning at", x, y, "to", x - 3, y + 3)
                    return True, value

        return False, value

    def get_action_space(self):
        return list(range(self.WIDTH))

    def reset(self):
        self.field = np.zeros(shape=(self.HEIGHT, self.WIDTH))
        self.steps = 0
        return self

    def get_state(self):
        return self.field

    def step(self, action):
        self.steps += 1
        if self.steps >= self.max_steps:
            #print("max steps")
            return self.field, 0, True, 0
        # get y coord:
        rev_y = reversed(range(self.HEIGHT))
        for y in rev_y:
            if self.field[y, action] == 0:
                self.move(action, y, 1)
                win, player = self.is_winning_state()
                if win and player == 1:
                    return self.field, 1, True, 1
                elif win and player == 2:
                    return self.field, -1, True, 2
                else:
                    possible = self.possible_positions()
                    move = possible[np.random.randint(0, len(possible))]
                    valid = self.move(move[0], move[1], 2)
                    win, who = self.is_winning_state()
                    if win and who == 2:
                        return self.field, -1, True, 2
                    else:
                        return self.field, 0, False, 0

        #print("invalid action")
        return self.field, 0, False, 0
