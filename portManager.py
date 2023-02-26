# Networks Assignments 1 - Port Manager

'''

'''

# These values specify the range of ports that can be used by clients
# Note that they can be changed by an admin to scale the app depemnding on load
low = 1000
high = 2000
# list of ports currently in use
used = []

# looks for new port for client to connect to


def getPort():
    for x in range(low, high):
        if x not in used:
            used.append(x)
            print("Client has connected on port", x)
            return x

# release port when client disconnects


def releasePort(portNumber):
    print("Client using port", portNumber, "has disconnected")
    used.remove(portNumber)
