import socket
import time
import threading
import random
controlHost = ""
PORT = 420


def clientThread():
    conn, addr = clientSocket.accept()
    t = threading.Thread(target=clientThread, daemon=True)
    t.start()
    with conn:
        print(f"Connected by {addr} on {PORT}")
        while True:
            conn.sendall(input("#").encode())
            data = conn.recv(1024)
            print(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # sock.bind((controlHost, controlPort)) # Server listens on 420 first
    # sock.listen()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.bind((controlHost, PORT))
        clientSocket.listen()
        while True:
            clientThread()
