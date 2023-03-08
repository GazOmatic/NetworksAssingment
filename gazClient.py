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
root = tkinter.Tk()
root.wm_withdraw()
DIRECTORY = getcwd()

# Define the address and port to connect to
print("Enter IP of server:")
server = input("#")
if len(server) == 0:
    server = 'localhost'
 # The remote host IP address

PORT = 3000       # The remote host port number
sending = True

# While loop to keep trying to connect to the server
while True:
    print("Attempting connection to server...")
    try:
        sock.connect((server, PORT))
        print("Connected!")
        break
    except ConnectionRefusedError:
        # If could not connect to server, keep retrying after 1 second
        sleep(1)
        continue
    except KeyboardInterrupt:
        break

# Create a connection manager
manager = connectionManager(True, sock)


def getFile(filename: str, dir: str):
    """
    Generates the GET header and sends it to the server. Takes in filename and directory. Returns a blank string if the file was not found
    """
    manager.send(f"GET#{filename}#")
    header = manager.receive()
    if type(header) == bytes:  # Make sure header is decoded.
        header = header.decode()
    header = header.split("#")  # Split the header with #
    sizeOfFile = header[0]
    sizeOfFile = int(sizeOfFile)
    if sizeOfFile == -1:  # If the size of the file is -1. Stop trying to get file. File does not exist
        print("404 - File not found")
        return ""
    print(f"Size is {sizeOfFile}")
    receivedBytes = 0
    with open(DIRECTORY + "/" + filename, "wb") as f:
        prev = 0
        while receivedBytes < sizeOfFile:
            chunk = manager.receiveBytes()
            f.write(chunk)
            receivedBytes += len(chunk)
            percent = round((receivedBytes/sizeOfFile)*100, 1)
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
        # Move to delete corrupted file, as it is of no use
        os.remove(DIRECTORY + "/" + filename)


def listServerFiles():
    """
    Sends the LIST header, gets the server reply and then lists the files
    """
    manager.send(f"LIST#{DIRECTORY}#")
    serverFiles = manager.receive().split("#")
    print("Server Direcory: \n")
    for f in serverFiles:
        print(f)

# Lists all files in client directory


def listLocalFiles():
    """
    List Files on the local directory
    """
    localFiles = os.listdir(DIRECTORY)
    out = ""
    for item in localFiles:
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
    manager.send(f"DELETE#{filename}#")


def uploadFile():
    """
    Client can specify a file to upload to the server. Client sends a POST command along with the file and then it is uploaded"""
    root = tkinter.Tk()
    root.wm_withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)

    filename = filedialog.askopenfilename()
    if filename == "":  # If no file given excape the function
        return
    try:
        checksum = getChecksum(filename)
        size = os.path.getsize(filename)
    except FileNotFoundError:
        manager.send("-1")
        return ""

    manager.send("POST#" + filename.split("/")
                 [-1] + "#" + str(size) + "#" + checksum)
    fiMan = fileManager(filename)
    while fiMan.chunk == fiMan.chunkSize:
        if manager.sendBytes(fiMan.getChunk()) == 0:
            break
    print("Successfully sent file " + filename)
    print(manager.receive())


def changeLocalDirectory():  # Promps the user to change directory
    global DIRECTORY
    print("Change Directory (c) or use default? (d)")
    a = input("#")
    if (a.lower() == 'c'):
        root.call('wm', 'attributes', '.', '-topmost', True)
        DIRECTORY = filedialog.askdirectory()
        if DIRECTORY == '':
            DIRECTORY = getcwd()
        chdir(DIRECTORY)
    elif (a.lower() == 'd'):
        return
    else:
        print("ERROR - Please input c for change or d for default")
    chdir('../')  # Move to directory 1 above


changeLocalDirectory()
print("Welcome to CLS File Sharing Platform")
print("Type (h) for list of commands")

# Command loop
userCommand = ''
while userCommand != 'q':
    userCommand = input("#")
    if len(userCommand) == 0:
        userCommand = ' '
    os.system("cls")  # Clear Screen
    if userCommand == 'd':
        listServerFiles()
        print("Enter Filename:")
        filename = input("#")
        if filename != '':
            getFile(filename, DIRECTORY)
    elif userCommand[0] == 'l':
        listServerFiles()
    elif userCommand[0] == 'u':
        uploadFile()
    elif userCommand[0] == 'm':
        listLocalFiles()
    elif userCommand[0] == 'r':
        listServerFiles()
        deleteFile()
    elif userCommand[0] == 'c':
        changeLocalDirectory()
    elif userCommand[0] == 'h':
        print("- HELP MENU -")
        print("- - - - - - - - - - - - -")
        print("UPLOAD\t\t\t(u)")
        print("DOWNLOAD\t\t(d)")
        print("SHOW REMOTE FILES\t(l)")
        print("LIST LOCAL FILES\t(m)")
        print("CHANGE LOCAL DIRECTORY\t(c)")
        print("HELP\t\t\t(h)")
        print("Quit\t\t\t(q)")
        print("- - - - - - - - - - - - -")

    elif userCommand != "q":
        print("Unknown Server Command - Type (h) for help")
