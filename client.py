import socket
import time
import os
from connectionManager import connectionManager
# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the address and port to connect to
host = 'localhost'  # The remote host IP address
port = 3000       # The remote host port number
sending = True
BATCH = 1024
sock.connect((host, port))

man = connectionManager(True, sock, BATCH)


def get(filename: str):
    print(man.next("GET#zero.py#"))


def listFiles(dir: str):
    fileList = ""
    files = os.listdir(dir)
    for f in files:
        fileList += f + "\n"


# Connect to the server
print("Welcome to CLS File Sharing Platform")
print("Type HELP for list of commands")


command = ''
while command != 'q':
    print("GET, LIST, TEST")
    command = input("#")
    if command == 'GET':
        get("Files/zero.py")
    if command == 'LIST':
        listFiles("C:\Users\richa\OneDrive\Desktop\Computer Science")
