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

numberOfErrors = 0
fixedErrors = 0
while True:
    incomingBytes = s.recv(4000)

    if incomingBytes == b'':
        print("\n\nERROR")
        break
    response = response_capnp.Response.from_bytes(incomingBytes)

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
           testNumber = 100
           break

    request = request_capnp.Request.new_message()
    bugFix = bugfix_capnp.Bugfix.new_message()

    if numberOfErrors > 0:
        fixedErrors += 1
    numberOfErrors -= 1

    if response.status == "Congratulation! You fixed all the bugs!":
        bugFix.bugs = fixedErrors;
        bugFix.message = "I solved a huge amount of bug. I am proud of myself."
    else:
        bugFix.message = "Fixed"
        bugFix.bugs = numberOfErrors

    request.bugfix = bugFix

    s.send(request.to_bytes())

    print("Sent bugfix message: " + bugFix.message)
    print("Sent bugfix bugs: " + str(bugFix.bugs))



