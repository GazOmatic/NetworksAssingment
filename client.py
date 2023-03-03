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
BATCH = 1024
sock.connect((host, port))

man = connectionManager(True, sock, BATCH)


def get(filename: str):
    print(man.send("GET#zero.py#"))
    
    size = man.receive(1024)
    print("Got size : " + size)
    f = man.receive(int(size.decode()))
    print(f)


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
        get("Files/zero.py")
    if command == 'LIST':
        listFiles()
