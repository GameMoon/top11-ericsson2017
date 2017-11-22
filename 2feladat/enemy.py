from env_helper_classes import Position
import random

class EnemyDir:
    vertical = ""
    horizontal = ""

class Enemy:
    position = None
    direction = None

    def __init__(self, enemies):
        self.position = Position()
        self.direction = EnemyDir()

        self.generate(enemies)

    def generate(self, enemies):
        self.create_position(enemies)
        self.create_start_dir()
        enemies.append(self)

    def create_position(self, enemies):
        pos_is_free = False
        x = -1
        y = -1
        while not pos_is_free:
            pos_is_free = True
            x = random.randint(2, 77)
            y = random.randint(2, 97)
            for enemy in enemies:
                if enemy.position.x == x and enemy.position.y == y:
                    pos_is_free = False
                    break

        self.position = Position(x, y)

    def create_start_dir(self):
        vertical_dir = ['up', 'down']
        horizontal_dir = ['left', 'right']
        if self.position.x == 0:
            vertical_dir.remove("up")
        if self.position.x == 79:
            vertical_dir.remove("down")
        if self.position.y == 0:
            horizontal_dir.remove("left")
        if self.position.y == 99:
            horizontal_dir.remove("right")
        v_dir = random.randint(0, len(vertical_dir)-1)
        h_dir = random.randint(0, len(horizontal_dir)-1)

        self.direction.vertical = vertical_dir[v_dir]
        self.direction.horizontal = horizontal_dir[h_dir]

    def move(self, cells):

        vertical_speed = 0
        if self.direction.vertical == 'down':
            vertical_speed = -1
        elif self.direction.vertical == 'up':
            vertical_speed = 1

        horizontal_speed = 0
        if self.direction.horizontal == 'left':
            horizontal_speed = -1
        elif self.direction.horizontal == 'right':
            horizontal_speed = 1

        new_x_pos = self.position.x + horizontal_speed
        new_y_pos = self.position.y + vertical_speed

        # if collision occur
        if cells[new_x_pos][new_y_pos].owner != 0:

            possible_actions = ['back', 'left', 'right']

            # Free escape positions
            free_x_pos = new_x_pos - 2 * horizontal_speed
            free_y_pos = new_y_pos - 2 * vertical_speed

            left_cell = cells[free_x_pos][new_y_pos]
            right_cell = cells[new_x_pos][free_y_pos]

            back_cell = cells[free_x_pos][free_y_pos]

            # Normal escape possibilities
            if free_x_pos in range(79) and left_cell.owner != 0:
                possible_actions.remove("left")
            if free_y_pos in range(99) and right_cell.owner != 0:
                possible_actions.remove("right")
            if free_y_pos in range(99) and free_x_pos in range(79) and back_cell.owner != 0:
                possible_actions.remove("back")

            # Strange escape possibilities
            if len(possible_actions) == 0:
                if free_x_pos in range(79) and cells[new_x_pos - 1 * horizontal_speed][new_y_pos].owner != 0:
                    possible_actions.append("back-left")
                if free_y_pos in range(99) and cells[new_x_pos][new_y_pos - 1 * vertical_speed].owner != 0:
                    possible_actions.append("back-right")

            # If no escape random direction
            if len(possible_actions) == 0:
                possible_actions = ['back', 'left', 'right']

            r_action = random.randint(0, len(possible_actions) - 1)

            current_h_dir = self.direction.horizontal
            current_v_dir = self.direction.vertical

            if possible_actions[r_action] == 'left' or possible_actions[r_action] == 'back-left':
                horizontal_speed *= -1
                self.direction.horizontal = self.reverse_direction(current_h_dir)

            if possible_actions[r_action] == 'right' or possible_actions[r_action] == 'back-right':
                vertical_speed *= -1
                self.direction.vertical = self.reverse_direction(current_v_dir)

            if possible_actions[r_action] == 'back':
                horizontal_speed *= -1
                vertical_speed *= -1
                self.direction.horizontal = self.reverse_direction(current_h_dir)
                self.direction.vertical = self.reverse_direction(current_v_dir)

        # update enemy position
        self.position.x = self.position.x + horizontal_speed
        self.position.y = self.position.y + vertical_speed

    def reverse_direction(self, direction):
        if direction == 'up':
            return 'down'
        elif direction == 'down':
            return 'up'
        elif direction == 'right':
            return 'left'
        elif direction == 'left':
            return 'right'
