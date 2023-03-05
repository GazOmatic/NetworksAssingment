import socket
import threading
import os
import time
import json
from connectionManager import connectionManager
from fileManager import fileManager, getChecksum
# Globals
controlHost = ""
PORT = 3000



def process(header: bytes, man: connectionManager):
    if type(header) == bytes:
        header = header.decode()
    comm = header.split("#")
    if comm[0] == "GET":
        try:
            size = os.path.getsize("Files/" + comm[1])
        except FileNotFoundError:
            man.send("-1")
            return ""
        checksum = getChecksum("Files/" + comm[1])
        man.send(str(size) + "#" + checksum)
        fm = fileManager("Files/" + comm[1])
        while fm.chunk == fm.chunkSize:
            if man.send(fm.getChunk()) == 0:
                break
        print("Successfully sent file " + comm[1])
        
    if comm[0] == "LIST":
        files = os.listdir(os.getcwd()+"/Files")
        out = ""
        for item in files:
            out += item + "#"
        man.send(out)
    if comm[0] == "POST":
        print("Preparing for upload")
        filename = comm[1]
        size = int(comm[2])
        if size == -1:
            print("404 - File not found")
            return ""
        print(f"Size is {size}")
        received = 0
        with open("Files/" + filename, "wb") as f:
            prev = 0
            while received < size:
                chunk = man.receive()
                f.write(chunk)
                received += len(chunk)
                percent = round((received/size)*100, 1)
                if percent - prev > 1:
                    print(f"{percent}%")
                    prev = percent
        checksum = getChecksum("Files/" + comm[1])
        if comm[3] == checksum:
            print("Checksum Match - File was not altered in transit")
            man.send("Success! - Checksum match")
        else:
            print("ERROR CHECKSUM MISMATCH - File was altered in Transit")
    if comm[0] == "DELETE":
        if comm[1] == '':
            return
        print("Deleting file " + comm[1])
        os.remove("Files/" + comm[1])
        
    if comm[0] == "PASSWORD":
        filename = comm[1]
        passcode = comm[2]
        
        files = {filename: passcode}
        
        #if file is not empty
        if os.path.isfile("passwords.json") and os.stat("passwords.json").st_size != 0:  
            with open("passwords.json", "r") as f:
                data = json.load(f)
            new_data = {filename:passcode}
            data.update(new_data)
            
            with open("passwords.json", "w") as f:
                json.dump(data, f)
            
        else: 
            with open("passwords.json", "w") as f:
                json.dump(files, f)


def clientThread(conn: socket.socket):
    with conn:
        # create a new connection manager and set to not sending
        man = connectionManager(False, conn)
        while True:
            out = man.receive()
            print(out)
            if out == 0:  # If it could not send the data, terminate the current thread
                break  # Escape the loop if message failed
            if not out:
                break
            process(out, man)


# Begining of the server

def main():
    global threads, controlHost
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.bind((controlHost, PORT))
        clientSocket.listen()
        while True:
            try:
                conn, addr = clientSocket.accept()
                print(f"Connected by {addr} on {PORT}")
                # When connection is created fork the thread and then repeat
                client = threading.Thread(target=clientThread, args=(conn,))
                client.daemon = True
                client.start()
                # Naming of threads for debugging reasons
                threads = threading.active_count()-1
                client.name = f"Client{threads}"
                print(f"Active Clients {threads}")
            except KeyboardInterrupt:
                print("Done")
                clientSocket.close()


if __name__ == "__main__":
    main()
