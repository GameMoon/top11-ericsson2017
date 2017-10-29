import capnp
import socket


request_capnp = capnp.load('Request.capnp')
response_capnp = capnp.load('Response.capnp')
bugfix_capnp = capnp.load('Bugfix.capnp')

request = request_capnp.Request.new_message()

request.login.team = "top11"
request.login.hash = "dp751bhpaaybmccx013r05r5ys084muj"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("ecovpn.dyndns.org", 11223))

s.send(request.to_bytes())


while True:
    response = response_capnp.Response.from_bytes(s.recv(1024))
    print("------------")
    print("--Received request message: " + response.status)
    print("--Received request type: " + response.which())

    if response.which() == 'bugfix':
        print("--Received bugfix message: " + response.bugfix.message)
        print("--Recieved bugfix bugs: " + str(response.bugfix.bugs))
        if response.bugfix.message != "":
            numberOfErrors = response.bugfix.bugs
    else:
        print("--Received end: " + str(response.end))
        if response.end:
           break


    request = request_capnp.Request.new_message()
    bugFix = bugfix_capnp.Bugfix.new_message()

    bugFix.message = "Fixed"


    if numberOfErrors > 0:
       numberOfErrors -= 1

    bugFix.bugs = numberOfErrors

    request.bugfix = bugFix

    s.send(request.to_bytes())
    print("Sent bugfix message: " + bugFix.message)
    print("Sent bugfix bugs: " + str(numberOfErrors))



