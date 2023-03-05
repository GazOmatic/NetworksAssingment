import socket
import time
import os
from connectionManager import connectionManager
from fileManager import fileManager, getChecksum
import tkinter
from tkinter import filedialog
from os import chdir, getcwd
# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the address and port to connect to
host = 'localhost'  # The remote host IP address
port = 3000       # The remote host port number
sending = True


while True:
    print("Attempting connection...")
    try:
        sock.connect((host, port))
        print("Connected!")
        break
    except ConnectionRefusedError:
        time.sleep(1)
        continue
    except KeyboardInterrupt:
        break


man = connectionManager(True, sock)


def get(filename: str, dir: str):
    man.send(f"GET#{filename}#")
    header = man.receive().decode().split("#")
    size = header[0]
    size = int(size)
    if size == -1:
        print("404 - File not found")
        return ""
    print(f"Size is {size}")
    received = 0
    with open(DIRECTORY +"/" + filename, "wb") as f:
        prev = 0
        while received < size:
            chunk = man.receive()
            f.write(chunk)
            received += len(chunk)
            percent = round((received/size)*100, 1)
            if percent - prev > 1:
                print(f"{percent}%")
                prev = percent
    checksum = getChecksum(DIRECTORY + filename)
    print(f"Local : {checksum} + Remote : {header[1]}")
    if header[1] == checksum:
        print("Checksum match")
        # print(f"Rec: {received} and size : {size} diff = {received-size}")


def listFiles():
    man.send(f"LIST#{dir}#")
    files = man.receive().decode().split("#")
    print("Server Direcory: \n")
    for f in files:
        print(f)

# Lists all files in client directory


def myFiles():
    files = os.listdir(DIRECTORY)
    out = ""
    for item in files:
        out += item + "\n"
    print("Local Directory: \n")
    print(out)


def deleteFile():
    print("Enter filename to remove:")
    filename = input(": ")
    man.send(f"DELETE#{filename}#")


def upload():
    root.call('wm', 'attributes', '.', '-topmost', True)
    filename = filedialog.askopenfilename()
    if filename == "":  # If no file given excape the function
        return
    try:
        checksum = getChecksum(filename)
        size = os.path.getsize(filename)
    except FileNotFoundError:
        man.send("-1")
        return ""
    man.send("POST#" + filename.split("/")
             [-1] + "#" + str(size) + "#" + checksum)
    fm = fileManager(filename)
    while fm.chunk == fm.chunkSize:
        if man.send(fm.getChunk()) == 0:
            break
    print("Successfully sent file " + filename)
    print(man.receive().decode())

root = tkinter.Tk()
root.wm_withdraw()
DIRECTORY = getcwd()
def changeDir():
    global DIRECTORY
    print("Change Directory (c) or use default? (d)")
    a = input("#")
    # set default directory to current directory
    #DIRECTORY = "R:/"
    
    if (a.lower() == 'c'):
        root.call('wm', 'attributes', '.', '-topmost', True)
        DIRECTORY = filedialog.askdirectory()
    # error checking
    elif (a.lower() == 'c'):
        pass
    # error checking
    else:
        print("ERROR - Please input c for change or d for default")
    dir = getcwd()
    print(dir)
    chdir('../')

changeDir()
# Connect to the server
print("Welcome to CLS File Sharing Platform")
print("Type (h) for list of commands")

command = ''
while command != 'q':
    command = input("#")
    if len(command) == 0:
        command = ' '
    os.system("cls")
    if command == 'd':
        listFiles()
        print("Enter Filename:")
        filename = input("#")
        if filename != '':
            get(filename, DIRECTORY)

    if command[0] == 'l':
        listFiles()
    if command[0] == 'u':
        upload()
    if command[0] == 'm':
        myFiles()
    if command[0] == 'r':
        listFiles()
        deleteFile()
    if command[0] == 'c':
        changeDir()
    if command[0] == 'h':
        print("HELP MENU\n----------------\nUpload - (u)\nDownload - (d)")
        print("List Server Directory - (l)\nList My Directory - (m)\nHelp - (h)")  # q,
        print("Change Directory - (c)")
