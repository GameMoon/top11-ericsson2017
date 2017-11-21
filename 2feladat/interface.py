import socket
import capnp


class CommunicationInterface:
    s = None
    common_capnp = capnp.load('Common.capnp')
    command_capnp = capnp.load('Command.capnp')
    response_capnp = capnp.load('Response.capnp')

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("epb2017.dyndns.org", 11224))

    def send(self, command):
        self.s.send(command.to_bytes_packed())

    def receive(self):
        read_bytes = self.s.recv(2000000)
        response = self.response_capnp.Response.from_bytes_packed(read_bytes)
        return response

    def login(self):
        command = self.command_capnp.Command.new_message()
        login = command.commands.init('login')
        login.team = "top11"
        login.hash = "dp751bhpaaybmccx013r05r5ys084muj"
        self.send(command)

    def send_command(self, moves):
        command = self.command_capnp.Command.new_message()
        moves_list = command.commands.init('moves', len(moves))
        for i in range(len(moves)):
            moves_list[i] = moves[i]
        self.send(command)

    def new_move(self, unit_id, direction):
        new_move = self.command_capnp.Move.new_message()
        new_move.unit = unit_id
        new_move.direction = direction
        return new_move
