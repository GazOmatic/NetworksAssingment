import socket
import time
import os
from connectionManager import connectionManager
from fileManager import fileManager
import tkinter
from tkinter import filedialog
from os import chdir, getcwd
# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the address and port to connect to
host = 'localhost'  # The remote host IP address
port = 3000       # The remote host port number
sending = True
sock.connect((host, port))

man = connectionManager(True, sock)


def get(filename: str, dir: str):
    print(man.send(f"GET#{filename}#"))
    size = man.receive(20)
    size = int(size.decode())
    if size == -1:
        print("404 - File not found")
        return ""
    print(f"Size is {size}")
    received = 0
    with open(DIRECTORY + filename, "wb") as f:
        while received < size:
            chunk = man.receive()
            f.write(chunk)
            received += len(chunk)
            print(f"{(received/size)*100}%")

        # print(f"Rec: {received} and size : {size} diff = {received-size}")


def listFiles():
    print(man.send(f"LIST#{dir}#"))
    files = man.receive().decode().split("#")
    for f in files:
        print(f)


print("Change Directory (c) or use default? (d)")
a = input("#")
# set default directory to current directory
DIRECTORY = getcwd()
#DIRECTORY = "R:/"

if (a.lower() == 'c'):
    root = tkinter.Tk()
    root.wm_withdraw()
    DIRECTORY = filedialog.askdirectory()
    root.destroy()
# error checking
elif (a.lower() == 'c'):
    pass
# error checking
else:
    print("ERROR - Please input c for change or d for default")
dir = getcwd()
print(dir)
chdir('../')

# Connect to the server
print("Welcome to CLS File Sharing Platform")
print("Type HELP for list of commands")


command = ''
while command != 'q':
    print("GET (g), LIST (l)")
    command = input("#")
    if command == 'g':
        get(input("Filename:"), DIRECTORY)

    if command == 'l':
        listFiles()
