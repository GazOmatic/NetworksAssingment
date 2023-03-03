import socket
import time
import os
from connectionManager import connectionManager
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
    size = int(man.receive(20).decode())-20
    received = 0
    with open(DIRECTORY + filename, "wb") as f:
        while received < size:
            received += man.BATCH
            f.write(man.receive())
            print(f"{(received/size)*100}%")
        print(f"Rec: {received} and size : {size} diff = {received-size}")


def listFiles():
    fileList = ""
    files = os.listdir(DIRECTORY)
    for f in files:
        fileList += f + "\n"

    print(fileList)


print("Change Directory or use default? (c/d)")
a = input(":")
# set default directory to current directory
DIRECTORY = getcwd()
DIRECTORY = "R:/"

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
    print("GET, LIST, TEST")
    command = input("#")
    if command == 'GET':
        get(input("Filename:"), DIRECTORY)

    if command == 'LIST':
        listFiles()
