# -*- coding: utf-8 -*-
from env_helper_classes import *

from enemy import Enemy
from unit import Unit

import random
import sys


class TestEnvironment:
    cells = []*80
    tick = 0
    level = 0
    owns = 1
    units = [Unit]
    enemies = [Enemy]

    def __init__(self):
        self.init()

    def init(self, level=0):
        self.tick = 0
        self.owns = 1
        self.cells = [None]*80
        self.already_checked = [[False for x in range(100)] for y in range(80)]

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

    def generate_units(self):
        for i in range(int(self.level/500)+1):
            Unit(self.units)

    def generate_enemies(self):
        for i in range(self.level+1-int(self.level/500)*480):
            Enemy(self.enemies)

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move(self.cells)

    def move_units(self, unit_movements):
        for unit_movement in unit_movements:
            conquering_done = self.units[unit_movement[0]].move(unit_movement[1], self.cells, self.units)
            if conquering_done:
                self.conquering_done(self.units[unit_movement[0]])

    def conquering_done(self, unit):
        for pos in unit.conquer_trail:  # Sets the trail to be our fields
            self.cells[pos.x][pos.y].__init__()
            self.cells[pos.x][pos.y].owner = self.owns
            self.cells[pos.x][pos.y].attack.unit = -1

        # Ahhoz, hogy egy cell-t csak egyszer nézzünk meg:
        for x in range(len(self.already_checked)):
            for y in range(len(self.already_checked[x])):
                if self.cells[x][y].owner == self.owns:
                    self.already_checked[x][y] = True
                else:
                    self.already_checked[x][y] = False

        for enemy in self.enemies:
            enemy_pos = Position(enemy.position.y, enemy.position.x)
            self.fill_area(enemy_pos, is_enemy=True)

        while len(unit.conquer_trail) > 0:
            pos = unit.conquer_trail.pop()

            self.fill_area(Position(pos.y+1, pos.x))
            self.fill_area(Position(pos.y-1, pos.x))
            self.fill_area(Position(pos.y, pos.x+1))
            self.fill_area(Position(pos.y, pos.x-1))

    # https://mail.python.org/pipermail/image-sig/2005-September/003559.html
    def fill_area(self, pos, is_enemy=False):
        if self.already_checked[pos.y][pos.x]:
            return
        edge = [(pos.x, pos.y)]
        self.already_checked[pos.y][pos.x] = True
        if not is_enemy:
            self.cells[pos.y][pos.x].owner = self.owns  # mienk a cell

        while edge:
            newedge = []
            for (x, y) in edge:
                for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    if not self.already_checked[t][s]:
                        self.already_checked[t][s] = True
                        if not is_enemy:
                            self.cells[t][s].owner = self.owns
                        newedge.append((s, t))
            edge = newedge

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

        damaged_units = []
        for unit in self.units:
            # unit out of the map
            if unit.position.x not in range(79) or unit.position.y not in range(99):
                if unit not in damaged_units:
                    unit.damage(self.cells)
                    damaged_units.append(unit)

        for enemy in self.enemies:
            # enemy collied with unit capturing line
            enemy_cell = self.cells[enemy.position.x][enemy.position.y]
            if enemy_cell.owner == 0 and enemy_cell.attack.which() == "unit":
                if self.units[enemy_cell.attack.unit] not in damaged_units:
                    self.units[enemy_cell.attack.unit].damage(self.cells)
                    damaged_units.append(self.units[enemy_cell.attack.unit])

            # enemy collied with unit
            for unit in self.units:
                if unit.position.x == enemy.position.x and unit.position.y == enemy.position.y:
                    if unit not in damaged_units:
                        unit.damage(self.cells)
                        damaged_units.append(unit)

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
        self.detect_collisions()

        if self.is_game_over():
            return False
        else:
            return True
