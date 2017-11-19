class Position:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

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

class EnemyDir:
    vertical = ""
    horizontal = ""

class Enemy:
    position = None
    direction = None

    def __init__(self):
        self.position = Position()
        self.direction = EnemyDir()

class Unit:
    owner = 0
    startpos = None
    position = None
    direction = ""
    health = 3
    killer = 6

    def __init__(self):
        self.position = Position()
        self.startpos = Position()

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
