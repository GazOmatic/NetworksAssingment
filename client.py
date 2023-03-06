import socket
from time import sleep
import os
import json
from connectionManager import connectionManager
from fileManager import fileManager, getChecksum
import tkinter
from tkinter import filedialog
from os import chdir, getcwd
# Create a socket object

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the address and port to connect to
print("Enter IP of server:")
host = input("#")
if len(host) == 0:
    host = 'localhost'
 # The remote host IP address

port = 3000       # The remote host port number
sending = True
protectedList = []
protected = False

# While loop to keep trying to connect to the server
while True:
    print("Attempting connection...")
    try:
        sock.connect((host, port))
        print("Connected!")
        break
    except ConnectionRefusedError:
        sleep(1)
        continue
    except KeyboardInterrupt:
        break

# Create a connection manager
man = connectionManager(True, sock)


def get(filename: str, dir: str):
    """
    Generates the GET header and sends it to the server. Takes in filename and directory. Returns a blank string if the file was not found
    """
    man.send(f"GET#{filename}#")
    header = man.receive()
    if type(header) == bytes:
        header = header.decode()
    header = header.split("#")
    size = header[0]
    size = int(size)
    if size == -1:
        print("404 - File not found")
        return ""
    print(f"Size is {size}")
    received = 0
    with open(DIRECTORY + "/" + filename, "wb") as f:
        prev = 0
        while received < size:
            chunk = man.receiveBytes()
            if type(chunk) == str:
                chunk = chunk.encode()
            f.write(chunk)
            received += len(chunk)
            percent = round((received/size)*100, 1)
            if percent - prev > 1:
                print(f"{percent}%")
                prev = percent
    checksum = getChecksum(DIRECTORY + "/" + filename)
    print(f"Local : {checksum} + Remote : {header[1]}")
    if header[1] == checksum:
        print("Checksum match")
        # print(f"Rec: {received} and size : {size} diff = {received-size}")
    else:
        print("ERROR CHECKSUM MISMATCH - File was altered in Transit")
        print("Removing Altered/Corrupted File")
        os.remove(DIRECTORY + "/" + filename)


def listFiles():
    """
    Sends the LIST header, gets the server reply and then lists the files
    """
    man.send(f"LIST#{DIRECTORY}#")
    files = man.receive().split("#")
    print("Server Direcory: \n")
    for f in files:
        print(f)

# Lists all files in client directory


def myFiles():
    """
    List Files on the local directory
    """
    files = os.listdir(DIRECTORY)
    out = ""
    for item in files:
        out += item + "\n"
    print(DIRECTORY)
    print("Local Directory: \n")
    print(out)


def deleteFile():
    """
    Deletes a file in the server directory by sending the server a delete command
    """
    print("Enter filename to remove:")
    filename = input(": ")
    man.send(f"DELETE#{filename}#")


def upload():
    """
    Client can specify a file to upload to the server. Client sends a POST command along with the file and then it is uploaded"""
    root = tkinter.Tk()
    root.wm_withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)

    # print("Is the file open (o) or protected (p)?:")
    # security = input("#")

    # if security == "p":
    #     print("Enter passcode:")
    #     passcode = input("#")
    #     protected = True

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
        if man.sendBytes(fm.getChunk()) == 0:
            break
    print("Successfully sent file " + filename)
    print(man.receive())


root = tkinter.Tk()
root.wm_withdraw()
DIRECTORY = getcwd()


def changeDir(): # Promps the user to change directory
    global DIRECTORY
    print("Change Directory (c) or use default? (d)")
    a = input("#")
    if (a.lower() == 'c'):
        root.call('wm', 'attributes', '.', '-topmost', True)
        DIRECTORY = filedialog.askdirectory()
        if DIRECTORY == '':
            DIRECTORY = getcwd()
        chdir(DIRECTORY)
    # error checking
    elif (a.lower() == 'd'):
        return
    # error checking
    else:
        print("ERROR - Please input c for change or d for default")
    # print(dir)
    chdir('../')


changeDir()
# Connect to the server
print("Welcome to CLS File Sharing Platform")
print("Type (h) for list of commands")

# Command loop
command = ''
while command != 'q':
    command = input("#")
    if len(command) == 0:
        command = ' '
    os.system("cls") # clear screen when command is successfull
    if command == 'd':
        listFiles()
        print("Enter Filename:")
        filename = input("#")
        if filename != '':
            get(filename, DIRECTORY)

    elif command[0] == 'l':
        listFiles()
    elif command[0] == 'u':
        upload()
    elif command[0] == 'm':
        myFiles()
    elif command[0] == 'r':
        listFiles()
        deleteFile()
    elif command[0] == 'c':
        changeDir()
    elif command[0] == 'h':
        print("HELP MENU\n----------------\nUpload - (u)\nDownload - (d)")
        print("List Server Directory - (l)\nList My Directory - (m)\nHelp - (h)")  # q,
        print("Change Directory - (c)\nQuit - (q)")
    elif command != "q":
        print("Unknown Server Command - Type (h) for help")
