# -*- coding: utf-8 -*-
from env_helper_classes import *
import random
from copy import deepcopy
import sys

class TestEnvironment:
    cells = []*80
    tick = 0
    level = 0
    owns = 1
    units = [Unit]
    enemies = [Enemy]

    def  __init__(self):
        self.init(0)

    def init(self, level):
        self.tick = 0
        self.owns = 1
        self.cells = [None]*80

        sys.setrecursionlimit(1000000)

        for x in range(len(self.cells)):
            self.cells[x] = [Cell]*100

        for x in range(len(self.cells)):
            for y in range(len(self.cells[x])):
                self.cells[x][y] = Cell()
                if x <= 1 or y <= 1 or x >= 78 or y >= 98:
                    self.cells[x][y].owner = self.owns

                else:
                    self.cells[x][y].owner = 0
                self.cells[x][y].attack.can = True

        self.level = level
        self.units = []
        self.enemies = []
        self.generate_units()
        self.generate_enemies()


    def get_free_unit_position(self):
        pos_is_free = False
        x = -1
        y = -1
        while not pos_is_free:
            pos_is_free = True
            x = random.randint(0, 79)
            y = random.randint(0, 99)
            for unit in self.units:
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

        new_pos = Position()
        new_pos.x = x
        new_pos.y = y
        return new_pos

    def get_free_enemy_position(self):
        pos_is_free = False
        x = -1
        y = -1
        while not pos_is_free:
            pos_is_free = True
            x = random.randint(2, 77)
            y = random.randint(2, 97)
            for enemy in self.enemies:
                if enemy.position.x == x and enemy.position.y == y:
                    pos_is_free = False
                    break

        new_pos = Position()
        new_pos.x = x
        new_pos.y = y
        return new_pos

    def get_free_position(self):
        pos_is_free = False
        x = -1
        y = -1
        while not pos_is_free:
            pos_is_free = True
            x = random.randint(0, 79)
            y = random.randint(0, 99)
            for enemy in self.enemies:
                if enemy.position.x == x and enemy.position.y == y:
                    pos_is_free = False
                    break
            for unit in self.units:
                if unit.position.x == x and unit.position.y == y:
                    pos_is_free = False
                    break
        new_pos = Position()
        new_pos.x = x
        new_pos.y = y
        return new_pos

    def get_random_unit_dir(self, position):
        possible_dirs = ['up', 'down', 'right', 'left']
        if position.x == 0:
            possible_dirs.remove("up")
        if position.x == 79:
            possible_dirs.remove("down")
        if position.y == 0:
            possible_dirs.remove("left")
        if position.y == 99:
            possible_dirs.remove("right")
        random_dir = random.randint(0, len(possible_dirs)-1)
        return possible_dirs[random_dir]

    def get_random_enemy_dir(self, position):
        vertical_dir = ['up', 'down']
        horizontal_dir = ['left', 'right']
        if position.x == 0:
            vertical_dir.remove("up")
        if position.x == 79:
            vertical_dir.remove("down")
        if position.y == 0:
            horizontal_dir.remove("left")
        if position.y == 99:
            horizontal_dir.remove("right")
        v_dir = random.randint(0, len(vertical_dir)-1)
        h_dir = random.randint(0, len(horizontal_dir)-1)
        return [vertical_dir[v_dir],horizontal_dir[h_dir]]

    def generate_units(self):
        for i in range(int(self.level/500)+1):
            new_unit = Unit()
            new_unit.owner = 1
            new_unit.position = self.get_free_unit_position()
            new_unit.direction = self.get_random_unit_dir(new_unit.position)
            new_unit.startpos.x = new_unit.position.x
            new_unit.startpos.y = new_unit.position.y
            self.units.append(new_unit)

    def generate_enemies(self):
        for i in range(self.level+1-int(self.level/500)*480):
            new_enemy = Enemy()
            new_enemy.position = self.get_free_enemy_position()
            dirs = self.get_random_enemy_dir(new_enemy.position)
            new_enemy.direction.vertical = dirs[0]
            new_enemy.direction.horizontal = dirs[1]
            self.enemies.append(new_enemy)

    def reverse_direction(self, direction):
        if direction == 'up':
            return 'down'
        elif direction == 'down':
            return 'up'
        elif direction == 'right':
            return 'left'
        elif direction == 'left':
            return 'right'

    def move_enemies(self):
        for enemyIndex in range(len(self.enemies)):
            vertical_speed = 0
            if self.enemies[enemyIndex].direction.vertical == 'down': vertical_speed = -1
            elif self.enemies[enemyIndex].direction.vertical == 'up': vertical_speed = 1

            horizontal_speed = 0
            if self.enemies[enemyIndex].direction.horizontal == 'left': horizontal_speed = -1
            elif self.enemies[enemyIndex].direction.horizontal == 'right': horizontal_speed = 1

            new_x_pos = self.enemies[enemyIndex].position.x+horizontal_speed
            new_y_pos = self.enemies[enemyIndex].position.y+vertical_speed

            # if collision occur
            if self.cells[new_x_pos][new_y_pos].owner != 0:

                possible_actions = ['back', 'left', 'right']

                # Free escape positions
                free_x_pos = new_x_pos-2*horizontal_speed
                free_y_pos = new_y_pos-2*vertical_speed

                left_cell = self.cells[free_x_pos][new_y_pos]
                right_cell = self.cells[new_x_pos][free_y_pos]

                back_cell = self.cells[free_x_pos][free_y_pos]

                # Normal escape possibilities
                if free_x_pos in range(79) and left_cell.owner != 0:
                    possible_actions.remove("left")
                if free_y_pos in range(99) and right_cell.owner != 0:
                    possible_actions.remove("right")
                if free_y_pos in range(99) and free_x_pos in range(79) and back_cell.owner != 0:
                    possible_actions.remove("back")

                # Strange escape possibilities
                if len(possible_actions) == 0:
                    if free_x_pos in range(79) and self.cells[new_x_pos - 1 * horizontal_speed][new_y_pos].owner != 0:
                        possible_actions.append("back-left")
                    if free_y_pos in range(99) and self.cells[new_x_pos][new_y_pos - 1 * vertical_speed].owner != 0:
                        possible_actions.append("back-right")

                # If no escape random direction
                if len(possible_actions) == 0:
                    possible_actions = ['back', 'left', 'right']

                r_action = random.randint(0, len(possible_actions) - 1)

                current_h_dir = self.enemies[enemyIndex].direction.horizontal
                current_v_dir = self.enemies[enemyIndex].direction.vertical

                if possible_actions[r_action] == 'left' or possible_actions[r_action] == 'back-left':
                    horizontal_speed *= -1
                    self.enemies[enemyIndex].direction.horizontal = self.reverse_direction(current_h_dir)

                if possible_actions[r_action] == 'right' or possible_actions[r_action] == 'back-right':
                    vertical_speed *= -1
                    self.enemies[enemyIndex].direction.vertical = self.reverse_direction(current_v_dir)

                if possible_actions[r_action] == 'back':
                    horizontal_speed *= -1
                    vertical_speed *= -1
                    self.enemies[enemyIndex].direction.horizontal = self.reverse_direction(current_h_dir)
                    self.enemies[enemyIndex].direction.vertical = self.reverse_direction(current_v_dir)

            # update enemy position
            self.enemies[enemyIndex].position.x = self.enemies[enemyIndex].position.x + horizontal_speed
            self.enemies[enemyIndex].position.y = self.enemies[enemyIndex].position.y + vertical_speed

    def move_units(self, unit_dirs):

        for dir in unit_dirs:
            unit_dir = Position()

            if dir[1] == 'up':
                unit_dir.x = -1
            elif dir[1] == 'down':
                unit_dir.x = 1

            if dir[1] == 'right':
                unit_dir.y = 1
            elif dir[1] == 'left':
                unit_dir.y = -1

        self.move_unit(self.units[dir[0]], unit_dir)

    def move_unit(self, unit, direction):
        if unit.health > 0:
            print("Direction: ", direction.x, direction.y)
            print(unit.position.x + direction.x, unit.position.y + direction.y)
            if (unit.position.x + direction.x) in range(100) and (unit.position.y + direction.y) in range(80):  # TODO: this should be somewhere else
                print(unit.position.x, unit.position.y)
                if (self.cells[unit.position.x][unit.position.y].owner == self.owns and  # Own field TODO: self.owns -> unit.owner
                   #self.cells[unit.position.x + direction.x][unit.position.y + direction.y].owner == 0 # Empty
                   self.cells[unit.position.x + direction.x][unit.position.y + direction.y].attack.can):  # Attackable field
                    unit.is_conquering = True

            if (unit.is_conquering and  # We are conquering this field
               self.cells[unit.position.x + direction.x][unit.position.y + direction.y].owner == unit.owner):  # Own field
                self.conquering_done(unit)
                unit.is_conquering = False

            unit.position.x = unit.position.x + direction.x
            unit.position.y = unit.position.y + direction.y

            if unit.is_conquering:
                self.cells[unit.position.x][unit.position.y].attack.unit = self.units.index(unit)  # TODO: set unit index
                # self.cells[unit.position.x][unit.position.y].attack.can = False  # TODO: kell ez?
                conquered_cell_pos = Position(unit.position.x, unit.position.y)
                unit.conquer_trail.append(conquered_cell_pos)  # Húzza a támadócsíkot

    def conquering_done(self, unit):
        for pos in unit.conquer_trail:  # Sets the trail to be our fields
            self.cells[pos.x][pos.y].__init__()
            self.cells[pos.x][pos.y].owner = self.owns
            self.cells[pos.x][pos.y].attack.unit = -1

        while len(unit.conquer_trail) > 0:
            pos = unit.conquer_trail.pop()

            # Try to fill neighbors
            tmp_cells = deepcopy(self.cells)
            if self.try_to_fill_area(tmp_cells, unit, Position(pos.x+1, pos.y)) != -1:
                self.cells = tmp_cells
            tmp_cells = deepcopy(self.cells)
            if self.try_to_fill_area(tmp_cells, unit, Position(pos.x-1, pos.y)) != -1:
                self.cells = tmp_cells
            tmp_cells = deepcopy(self.cells)
            if self.try_to_fill_area(tmp_cells, unit, Position(pos.x, pos.y+1)) != -1:
                self.cells = tmp_cells
            tmp_cells = deepcopy(self.cells)
            if self.try_to_fill_area(tmp_cells, unit, Position(pos.x, pos.y-1)) != -1:
                self.cells = tmp_cells

    def try_to_fill_area(self, tmp_cells, unit, pos):
        for enemy in self.enemies:
            if enemy.position.x == pos.x and enemy.position.y == pos.y:  # if enemy
                return -1

        if tmp_cells[pos.x][pos.y].owner == self.owns:  # mienk a cell
            return 0
        tmp_cells[pos.x][pos.y].owner = self.owns
        tmp_cells[pos.x][pos.y].attack.unit = -1

        if (self.try_to_fill_area(tmp_cells, unit, Position(pos.x+1, pos.y)) == -1
            or self.try_to_fill_area(tmp_cells, unit, Position(pos.x, pos.y-1)) == -1
            or self.try_to_fill_area(tmp_cells, unit, Position(pos.x-1, pos.y)) == -1
            or self.try_to_fill_area(tmp_cells, unit, Position(pos.x, pos.y+1)) == -1):
            return -1
        return 0

    def receive(self):
        response = Response()
        response.info.level = self.level
        response.info.tick = self.tick
        response.info.owns = self.owns
        response.cells = self.cells
        response.units = self.units
        response.enemies = self.enemies
        return response

    def detect_collisions(self):

        for unit_index in range(len(self.units)):
            # unit out of the map
            if not self.units[unit_index].position.x in range(79) or not self.units[unit_index].position.x in range(99):
                self.damage_unit(unit_index)
                continue

            if self.units[unit_index].position.x in range(79) and self.units[unit_index].position.x in range(99):
                # unit collied with own capturing line
                unit_cell = self.cells[self.units[unit_index].position.x][self.units[unit_index].position.y]

            if unit_cell.attack.which() == "unit" and unit_cell.attack.unit == unit_index:
                self.damage_unit(unit_index)

        for enemy in self.enemies:
            enemy_cell = self.cells[enemy.position.x][enemy.position.y]
            # enemy collied with unit capturing line
            # if enemy_cell.owner == 0 and enemy_cell.attack.which() == "unit":
            #     self.damage_unit(enemy_cell.attack.unit)

            # enemy collied with unit
            for unit_index in range(len(self.units)):
                if self.units[unit_index].position.x == enemy.position.x and self.units[unit_index].position.y == enemy.position.y:
                    self.damage_unit(unit_index)

    def damage_unit(self, unit_index):
        self.units[unit_index].position.x = self.units[unit_index].startpos.x
        self.units[unit_index].position.y = self.units[unit_index].startpos.y

        if self.units[unit_index].health > 0:
            self.units[unit_index].health -= 1

    def is_level_finished(self):
        number_of_owned_cells = 0
        for cell_row in self.cells:
            for cell in cell_row:
                if cell.owner == 1:
                    number_of_owned_cells += 1

        if number_of_owned_cells/(80*100) > 0.75:
            return True
        else:
            return False

    def is_game_over(self):
        dead_units = 0
        for unit in self.units:
            if unit.health == 0:
                dead_units += 1

        if dead_units == len(self.units):
            return True
        else:
            return False

    def update(self, directions):
        self.tick = self.tick + 1
        self.move_units(directions)  # mozgat és a foglalást is figyeli!

        if self.is_level_finished():
            self.init(self.level+1)

        self.move_enemies()
        #self.detect_collisions()

        if self.is_game_over():
            return False
        else:
            return True
