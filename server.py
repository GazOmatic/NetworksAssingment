import socket
import threading
import os
import time
import json
from connectionManager import connectionManager
from fileManager import fileManager, getChecksum
# Globals
controlHost = "0.0.0.0"
PORT = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = (s.getsockname()[0])
s.close()
print(f"Server IP : {ip}")
print()
print("Waiting for clients...")


def process(header: bytes, man: connectionManager):
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
    elif comm[0] == "LIST":
        files = os.listdir(os.getcwd()+"/Files")
        out = ""
        for item in files:
            out += item + "#"
        man.send(out)
    elif comm[0] == "POST":
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
            print("Removing Altered/Corrupted File")
            os.remove("Files/" + filename)
    elif comm[0] == "DELETE":
        if comm[1] == '':
            return
        print("Deleting file " + comm[1])
        try:
            os.remove("Files/" + comm[1])
        except FileNotFoundError:
            print("ERROR 404 - File not found")
    else:
        print("Invalid header")
        man.send("ERROR - INVALID HEADER")


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
                print()


if __name__ == "__main__":
    main()
