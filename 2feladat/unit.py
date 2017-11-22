from env_helper_classes import Position
import random


class Unit:
    owner = 0
    startpos = None
    position = None
    direction = ""
    health = 3
    killer = 6
    is_conquering = False
    conquer_trail = []

    def __init__(self, units):
        self.position = Position()
        self.startpos = Position()

        self.generate(units)

    def generate(self, units):
        self.owner = 1
        self.position = Position(0, 0)
        # self.create_position(units)
        self.create_start_dir()
        self.startpos = Position(self.position.x, self.position.y)
        units.append(self)

    def create_position(self, units):
        pos_is_free = False
        x = -1
        y = -1
        while not pos_is_free:
            pos_is_free = True
            x = random.randint(0, 79)
            y = random.randint(0, 99)
            for unit in units:
                if unit.position.x == x and unit.position.y == y:
                    pos_is_free = False
                    break

        which_site = random.randint(0, 3)  # top, bottom, left or right side
        if which_site == 0:
            x = 0
        elif which_site == 1:
            x = 79
        elif which_site == 2:
            y = 0
        elif which_site == 3:
            y = 99

        self.position = Position(x, y)

    def create_start_dir(self):
        possible_dirs = ['up', 'down', 'right', 'left']
        if self.position.x == 0:
            possible_dirs.remove("up")
        if self.position.x == 79:
            possible_dirs.remove("down")
        if self.position.y == 0:
            possible_dirs.remove("left")
        if self.position.y == 99:
            possible_dirs.remove("right")
        random_dir = random.randint(0, len(possible_dirs) - 1)

        self.direction = possible_dirs[random_dir]

    def move(self, direction_text, cells, units):

        direction = Position()

        if direction_text == 'up':
            direction.x = -1
        elif direction_text == 'down':
            direction.x = 1

        if direction_text == 'right':
            direction.y = 1
        elif direction_text == 'left':
            direction.y = -1

        conquering_done = False

        if self.health > 0:
            # TODO: this should be somewhere else
            if (self.position.x + direction.x) in range(100) and (self.position.y + direction.y) in range(80):
                # if (cells[self.position.x][self.position.y].owner == self.owner and  # Own field
                #     cells[self.position.x + direction.x][self.position.y + direction.y].attack.can): # Attackable field
                #     self.is_conquering = True

                # állandoan húzza a vonalat
                if (cells[self.position.x][self.position.y].attack.can): # Attackable field
                    self.is_conquering = True

            if (self.is_conquering and  # We are conquering this field
                cells[self.position.x + direction.x][self.position.y + direction.y].owner == self.owner):  # Own field

                conquering_done = True
                self.is_conquering = False

            self.position.x = self.position.x + direction.x
            self.position.y = self.position.y + direction.y

            if self.is_conquering:
                cells[self.position.x][self.position.y].attack.unit = units.index(self)
                conquered_cell_pos = Position(self.position.x, self.position.y)
                self.conquer_trail.append(conquered_cell_pos)  # Húzza a támadócsíkot

            return conquering_done

    def damage(self, cells):
        for pos in self.conquer_trail:  # Sets the trail to be our fields
            cells[pos.x][pos.y].owner = 0
            cells[pos.x][pos.y].attack.unit = -1
            cells[pos.x][pos.y].attack.can = True

        self.conquer_trail = []
        self.is_conquering = False

        self.position.x = self.startpos.x
        self.position.y = self.startpos.y

        if self.health > 0:
            self.health -= 1
