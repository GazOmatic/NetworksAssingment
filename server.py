import socket
import threading
import os
import time
from connectionManager import connectionManager
# Globals
controlHost = ""
PORT = 3000
BATCH = 1024
threads = 0


def clientThread(conn: socket.socket):
    global threads
    with conn:
        # create a new connection manager and set to not sending
        man = connectionManager(False, conn, BATCH)
        while True:
            out = man.next("Hello world")   
            if out == 0:  # If it could not send the data, terminate the current thread
                threads = threads - 1  # Decrement the thread count
                break  # Escape the loop if message failed


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
                client.name = f"Client{threads}"
                threads = threads + 1
                print(f"Active Clients {threads}")
            except KeyboardInterrupt:
                print("Done")
                clientSocket.close()


if __name__ == "__main__":
    main()
