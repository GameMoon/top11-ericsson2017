# -*- coding: utf-8 -*-
from interface import CommunicationInterface
from converter import OutputGenerator
from test_env import TestEnvironment

from env_helper_classes import *

from pynput import keyboard

direction = "right"


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
interface = CommunicationInterface()
interface.login()
# A szervertől érkező adatokat konvertálja, megjeleníti
generator = OutputGenerator()

with keyboard.Listener(
        on_press=on_press) as listener:

    while True:
        response = interface.receive()
        interface.send_command([interface.new_move(0, direction)])
        print("Level: ", response.info.level, " Tick: ", response.info.tick)
        output = generator.convert(response.cells, response.units, response.enemies)
        generator.show(output)

    listener.join()