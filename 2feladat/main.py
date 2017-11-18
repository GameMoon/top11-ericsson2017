from interface import CommunicationInterface
from converter import OutputGenerator

interface = CommunicationInterface()
generator = OutputGenerator()

interface.login()


for i in range(30):

    response = interface.receive()
    interface.send_command([interface.new_move(0, 'right')])
    output = generator.convert(response.cells, response.units, response.enemies)
    generator.show(output)
    #generator.create_image(output, response.info.tick)

for i in range(80):

    response = interface.receive()
    interface.send_command([interface.new_move(0, 'down')])
    output = generator.convert(response.cells, response.units, response.enemies)
    generator.show(output)
    #generator.create_image(output,response.info.tick)



