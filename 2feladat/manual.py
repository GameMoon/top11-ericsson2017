# -*- coding: utf-8 -*-
from interface import CommunicationInterface
from converter import OutputGenerator
from test_env import TestEnvironment

from env_helper_classes import *

from pynput import keyboard
import time

direction = "right"

test_env = TestEnvironment()


def on_press(key):
    global direction
    try:
        if key == keyboard.Key.up:
            direction = "up"
        elif key == keyboard.Key.down:
            direction = "down"
        elif key == keyboard.Key.right:
            direction = "right"
        elif key == keyboard.Key.left:
            direction = "left"
    except AttributeError:
        print('special key {0} pressed'.format(key))


# kommunikál a szerverrel
#interface = CommunicationInterface()
#interface.login()
# A szervertől érkező adatokat konvertálja, megjeleníti
generator = OutputGenerator()

with keyboard.Listener(
        on_press=on_press) as listener:

    while True:
        #interface.send_command([interface.new_move(0, direction)])
        #response = interface.receive()
        response = test_env.receive()

        is_running = test_env.update([[0, direction]])
        if not is_running:
            break
        print("Level: ", response.info.level, " Tick: ", response.info.tick," HP: ", response.units[0].health)
        output = generator.convert(response.cells, response.units, response.enemies)
        time.sleep(0.05)
        generator.show(output)
    print("end")
    listener.join()
