from enum import Enum

class Direction(Enum):
    down: 0
    up: 1
    left: 2
    right: 3

class Position:
    x = 0
    y = 0

class Attack:
    can = True
    unit = -1
    def which(self):
        if self.unit == -1:
            return 'can'
        else:
            return 'unit'
class Cell:
    owner = 0
    attack = None

    def __init__(self):
        self.attack = Attack()

class Enemy:
    position = Position
    direction = {'vertical': "", 'horizontal': ""}

class Unit:
    owner = 0
    startpos = Position
    position = Position
    direction = ""
    health = 3
    killer = 6

class Info:
    owns = 1
    level = 0
    tick = 0
class Response:
    status = "status"
    info = Info
    cells = [Cell]
    enemies = [Enemy]
    units = [Unit]
