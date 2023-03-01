import socket
import threading
import os
import connectionManager
controlHost = ""
PORT = 3000

BATCH = 1024
threads = []


def clientThread(conn: socket.socket):
    with conn:
        print(f"Connected by {addr} on {PORT}")
        man = connectionManager(False,conn,BATCH) # create a new connection manager and set to not sending
        man.sen



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    clientSocket.bind((controlHost, PORT))
    clientSocket.listen()
    while True:
        try:
            conn, addr = clientSocket.accept()
            print(type(conn))
            # When connection is created fork the thread and then repeat
            t = threading.Thread(target=clientThread, args=(conn,))
            t.daemon = True
            t.start()
            threads.append(t)
            print(len(threads))
        except KeyboardInterrupt:
            print("Done")
            clientSocket.close()
