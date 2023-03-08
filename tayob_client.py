import socket
import time
import os
import json
from connectionManager import connectionManager
from fileManager import fileManager, getChecksum
import tkinter
from tkinter import filedialog
from os import chdir, getcwd

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the address and port
host = 'localhost'  # The remote host IP address
port = 3000       # The remote host port number
sending = True
protected = False


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


connManager = connectionManager(True, sock)


def get(filename: str, dir: str):
  
   
    #open and load json file
    with open(DEFAULT_DIR + "/" +'passwords.json', 'r') as f:
        file_passwords = json.load(f)
        
    #check if file is protected by checking if it's in json file
    file_to_find = filename
    
    if file_to_find in file_passwords:
        print(f"File is protected")
        passcode = input("Enter passcode:")
        
        if passcode == file_passwords[file_to_find]:
            print("Password is correct")
        else: 
            print("Password is incorrect")
            return ""      
  
    
    connManager.send(f"GET#{filename}#")
    header = connManager.receive().decode().split("#")
    size = header[0]
    size = int(size)
    if size == -1:
        print("404 - File not found")
        return ""
    #print(f"Size is {size}")
    received = 0
    
    with open(DIRECTORY + filename, "wb") as f:
        prev = 0
        while received < size:
            chunk = connManager.receive()
            f.write(chunk)
            received += len(chunk)
            percent = round((received/size)*100, 1)
            if percent - prev > 1:
                #print(f"{percent}%")
                prev = percent
    checksum = getChecksum(DIRECTORY + filename)
    
    print(f"Local : {checksum} + Remote : {header[1]}")
    if header[1] == checksum:
        print("Checksum match")


def listFiles():
    connManager.send(f"LIST#{dir}#")
    files = connManager.receive().decode().split("#")
    print("Server Direcory: \n")
    for f in files:
        print(f)


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
    
    with open(DEFAULT_DIR + "/" +'passwords.json', 'r') as f:
        file_passwords = json.load(f)
        
   
    file_to_find = filename
    
     #check if file is protected
    if file_to_find in file_passwords:
        print(f"File is protected")
        passcode = input("Enter passcode:")
        
        if passcode == file_passwords[file_to_find]:
            print("Password is correct")
            connManager.send("DELETE_PASSWORD#" + os.path.basename(filename) + "#" + passcode)
            
        else: 
            print("Password is incorrect")
            return ""
    
    connManager.send(f"DELETE#{filename}#")


def upload():
    root = tkinter.Tk()
    root.wm_withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    protected = False
    
    print("Is the file open (o) or protected (p)?:")
    security = input("#")
    
    if security == "p":
        print("Enter passcode:")
        passcode = input("#")
        protected = True
    
    elif security == "o":
        pass
    
    else:
        return
    

    filename = filedialog.askopenfilename()
    
    if filename == "":  # If no file given excape the function
        return
  
    try:
        checksum = getChecksum(filename)
        size = os.path.getsize(filename)
    except FileNotFoundError:
        connManager.send("-1")
        return ""        
    
    connManager.send("POST#" + filename.split("/")
             [-1] + "#" + str(size) + "#" + checksum)
    fm = fileManager(filename)
    while fm.chunk == fm.chunkSize:
        if connManager.send(fm.getChunk()) == 0:
            break
    print("Successfully sent file " + filename)
    print(connManager.receive().decode())
    
    if protected == True:
        connManager.send("UPLOAD_PASSWORD#" + os.path.basename(filename) + "#" + passcode)
        protected = False

root = tkinter.Tk()
root.wm_withdraw()
DIRECTORY = getcwd()
DEFAULT_DIR = DIRECTORY

def changeDir():
    
    #global DIRECTORY
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
    # error checking
    else:
        print("ERROR - Please input c for change or d for default")

    #chdir('../')
    


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
        print("HELP MENU\n----------------\nUpload - (u)\nDownload - (d)\nRemove - (r)")
        print("List Server Directory - (l)\nList My Directory - (m)\nHelp - (h)")  # q,
        print("Change Directory - (c)")
