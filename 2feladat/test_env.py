# -*- coding: utf-8 -*-
from env_helper_classes import *
import random

class TestEnvironment:
    cells = []*80
    tick = 0
    level = 0
    owns = 1
    units = [Unit]
    enemies = [Enemy]

    def  __init__(self):
        self.init(-1)

    def init(self, level):
        self.tick = 0
        self.owns = 1
        self.cells = [None]*80

        for x in range(len(self.cells)):
            self.cells[x] = [Cell]*100

        for x in range(len(self.cells)):
            for y in range(len(self.cells[x])):
                self.cells[x][y] = Cell()
                if x == 0 or y == 0 or x == 79 or y == 99:
                    self.cells[x][y].owner = self.owns

                else:
                    self.cells[x][y].owner = 0
                self.cells[x][y].attack.can = True

        self.level = level + 1
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
            x = random.randint(1, 78)
            y = random.randint(1, 98)
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

    def get_random_unit_dir(self,position):
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

    def get_random_enemy_dir(self,position):
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
            new_unit.startpos = new_unit.position
            self.units.append(new_unit)

    def generate_enemies(self):

        for i in range(self.level+1-int(self.level/500)*480):
            new_enemy = Enemy()
            new_enemy.position = self.get_free_enemy_position()
            dirs = self.get_random_enemy_dir(new_enemy.position)
            new_enemy.direction['vertical'] = dirs[0]
            new_enemy.direction['horizontal'] = dirs[1]
            self.enemies.append(new_enemy)

    def move_enemies(self):
        for enemyIndex in range(len(self.enemies)):
            vertical_speed = 0
            if self.enemies[enemyIndex].direction['vertical'] == 'down': vertical_speed = -1
            elif self.enemies[enemyIndex].direction['vertical'] == 'up': vertical_speed = 1

            horizontal_speed = 0
            if self.enemies[enemyIndex].direction['horizontal'] == 'left': horizontal_speed = -1
            elif self.enemies[enemyIndex].direction['horizontal'] == 'right': horizontal_speed = 1

            new_x_pos = self.enemies[enemyIndex].position.x+horizontal_speed
            new_y_pos = self.enemies[enemyIndex].position.y+vertical_speed

            # nincs ütközés
            if self.cells[new_x_pos][new_y_pos].owner == 0:
                self.enemies[enemyIndex].position.x = self.enemies[enemyIndex].position.x+horizontal_speed
                self.enemies[enemyIndex].position.y = self.enemies[enemyIndex].position.y+vertical_speed
            else:
                possible_actions = ['back', 'left', 'right']
                if new_x_pos-2*horizontal_speed in range(79) and self.cells[new_x_pos-2*horizontal_speed][new_y_pos].owner != 0:
                    possible_actions.remove("left")
                if new_y_pos-2*vertical_speed in range(99) and self.cells[new_x_pos ][new_y_pos-2*vertical_speed].owner != 0:
                    possible_actions.remove("right")
                if new_y_pos-2*vertical_speed in range(99) and new_x_pos-2*horizontal_speed in range(79) and self.cells[new_x_pos-2*horizontal_speed][new_y_pos - 2 * vertical_speed].owner != 0:
                    possible_actions.remove("back")

                if len(possible_actions) == 0:
                    if new_x_pos-2*horizontal_speed in range(79) and self.cells[new_x_pos - 1 * horizontal_speed][new_y_pos].owner != 0:
                        possible_actions.append("back-left")
                    if new_y_pos-2*vertical_speed in range(99) and self.cells[new_x_pos][new_y_pos - 1 * vertical_speed].owner != 0:
                        possible_actions.append("back-right")

                if len(possible_actions) == 0:
                    pass
                else:
                    r_action = random.randint(0, len(possible_actions) - 1)
                    if possible_actions[r_action] == 'left':
                        horizontal_speed = horizontal_speed*-1
                        if self.enemies[enemyIndex].direction['horizontal'] == 'left':
                            self.enemies[enemyIndex].direction['horizontal'] = 'right'
                        else:
                            self.enemies[enemyIndex].direction['horizontal'] = 'left'
                    if possible_actions[r_action] == 'right':
                        vertical_speed = vertical_speed*-1
                        if self.enemies[enemyIndex].direction['vertical'] == 'up':
                            self.enemies[enemyIndex].direction['vertical'] = 'down'
                        else:
                            self.enemies[enemyIndex].direction['vertical'] = 'up'
                    if possible_actions[r_action] == 'back':
                        horizontal_speed = horizontal_speed*-1
                        vertical_speed = vertical_speed * -1
                        if self.enemies[enemyIndex].direction['horizontal'] == 'left':
                            self.enemies[enemyIndex].direction['horizontal'] = 'right'
                        else:
                            self.enemies[enemyIndex].direction['horizontal'] = 'left'
                        if self.enemies[enemyIndex].direction['vertical'] == 'up':
                            self.enemies[enemyIndex].direction['vertical'] = 'down'
                        else:
                            self.enemies[enemyIndex].direction['vertical'] = 'up'

                self.enemies[enemyIndex].position.x = self.enemies[enemyIndex].position.x + horizontal_speed
                self.enemies[enemyIndex].position.y = self.enemies[enemyIndex].position.y + vertical_speed

    def move_units(self, directions):
        which_unit = 0
        for dir in directions:
            self.move_unit(self.units[which_unit], dir)
            which_unit += 1

    def move_unit(self, unit, direction):
        unit.position.x = unit.position.x + direction.x
        unit.position.y = unit.position.y + direction.y

    def receive(self):
        response = Response()
        response.info.level = self.level
        response.info.tick = self.tick
        response.info.owns = self.owns
        response.cells = self.cells
        response.units = self.units
        response.enemies = self.enemies
        return response

    def update(self):
        self.tick = self.tick + 1
        self.move_enemies()


