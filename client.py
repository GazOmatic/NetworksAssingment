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

man = connectionManager(True, sock)

def get(filename: str, dir: str):
    # with open(DIRECTORY + "/" +'passwords.json', 'r') as f:
    #     file_passwords = json.load(f)      
    # #check if file is protected
    # file_to_find = filename
    
    # if file_to_find in file_passwords:
    #     print(f"File is protected")
    #     passcode = input("Enter passcode:")
        
    #     if passcode == file_passwords[file_to_find]:
    #         print("Password is correct")
    #     else: 
    #         print("Password is incorrect")
    #         return ""      
  
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
            chunk = man.receive()
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
    man.send(f"LIST#{DIRECTORY}#")
    files = man.receive().split("#")
    print("Server Direcory: \n")
    for f in files:
        print(f)

# Lists all files in client directory


def myFiles():
    files = os.listdir(DIRECTORY)
    out = ""
    for item in files:
        out += item + "\n"
    print(DIRECTORY)
    print("Local Directory: \n")
    print(out)


def deleteFile():
    print("Enter filename to remove:")
    filename = input(": ")
    man.send(f"DELETE#{filename}#")


def upload():
    root = tkinter.Tk()
    root.wm_withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    
    print("Is the file open (o) or protected (p)?:")
    security = input("#")
    
    if security == "p":
        print("Enter passcode:")
        passcode = input("#")
        protected = True 
    
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
    
    if protected == True:
        man.send("PASSWORD#" + os.path.basename(filename) + "#" + passcode)


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
        if DIRECTORY == '':
            DIRECTORY = getcwd()
        chdir(DIRECTORY) #
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
