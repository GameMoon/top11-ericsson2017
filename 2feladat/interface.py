import socket
import capnp


class CommunicationInterface:
    s = None
    common_capnp = capnp.load('Common.capnp')
    command_capnp = capnp.load('Command.capnp')
    response_capnp = capnp.load('Response.capnp')

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("ecovpn.dyndns.org", 11224))

    def send(self, command):
        self.s.send(command.to_bytes())

    def receive(self):
        read_bytes = b''
        while True:
            incoming_bytes = self.s.recv(2000)
            read_bytes += incoming_bytes

            try:
                response = self.response_capnp.Response.from_bytes(read_bytes)
                break
            except:
                pass
        return response

    def login(self):
        command = self.command_capnp.Command.new_message()
        login = command.commands.init('login')
        login.team = "top11"
        login.hash = "dp751bhpaaybmccx013r05r5ys084muj"
        self.send(command)

