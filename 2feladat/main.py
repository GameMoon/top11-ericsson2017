from interface import CommunicationInterface

interface = CommunicationInterface()

interface.login()

response = interface.receive()
print(response.status)

