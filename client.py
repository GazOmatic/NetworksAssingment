import socket
import time
# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the address and port to connect to
host = 'localhost'  # The remote host IP address
port = 3000       # The remote host port number
sending = True

BATCH = 1024
sock.connect((host, port))

def receive(data:str):
    if sending == True:
        return send(data)
    else:
      return sock.recv(BATCH).decode()  

def send(data:str):
    print()
    if sending == False:
        return receive()
    else:
        return sock.sendall(data.encode())

def get(filename:str):
    print()

# Connect to the server
print("Welcome to CLS File Sharing Platform")
print("Type HELP for list of commands")


command = ''
while command != 'q':
    print("GET, LIST, TEST")
    command = input("#")
    if command == 'GET':
          get("Files/zero.py")
