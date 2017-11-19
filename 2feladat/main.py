from interface import CommunicationInterface
from converter import OutputGenerator
from test_env import TestEnvironment

from env_helper_classes import *

# kommunikál a szerverrel
#interface = CommunicationInterface()
# A szervertől érkező adatokat konvertálja, megjeleníti
generator = OutputGenerator()
# teszt környezet
test_env = TestEnvironment()


#test_env.send([interface.new_move(0, 'right')])
#interface.login()

#response = interface.receive()

for i in range(100):
    response = test_env.receive()
    stateVector = generator.convert(response.cells, response.units, response.enemies)
    generator.create_image(stateVector, response.info.tick)
    test_env.update()
#print(str(response.units[0].position.x)+" | "+str(response.units[0].position.y)+" | "+str(response.units[0].direction) + " | "+ str(response.units[0].health))
#print(str(response.enemies[0].position.x)+" | "+str(response.enemies[0].position.y)+" | "+str(response.enemies[0].direction))



#test_env.update("up",stateVector)

# for i in range(30):
#
#     response = interface.receive()
#     interface.send_command([interface.new_move(0, 'right')])
#     output = generator.convert(response.cells, response.units, response.enemies)
#     #generator.create_image(output, response.info.tick)
#
# for i in range(80):
#
#     response = interface.receive()
#     interface.send_command([interface.new_move(0, 'down')])
#     output = generator.convert(response.cells, response.units, response.enemies)
#     #generator.create_image(output,response.info.tick)



