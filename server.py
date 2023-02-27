import socket
import time
import threading
import random
from portManager import *
controlHost = ""
controlPort = 420


def clientThread(newPort):
    print("stuff")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.bind((controlHost, newPort))
        clientSocket.listen()
        conn, addr = clientSocket.accept()
        with conn:
            print(f"Connected by {addr} on {newPort}")
            while True:
                #
                try:
                    conn.sendall(input("#").encode())
                    data = conn.recv(1024)
                    print(data)

                except ConnectionResetError:
                    print(f"Client on port {newPort} disconnected")
                    releasePort(newPort)


# This function is what will determine what ports are available and can be used for a new client.
def negotiate(conn):
    currentPort = getPort()
    conn.sendall(f"PORT:{currentPort}".encode())
    t = threading.Thread(target=clientThread, daemon=True, args=(currentPort,))
    t.start()
    return True


def server(sock, HOST, PORT):  # Server accepts any incoming connection
    conn, addr = sock.accept()
    with conn:
        print(f"Connected by {addr} on {PORT}")
        while True:
            # If a client connects to control port (420) It means it neads to negotiate a new port
            if PORT == 420:
                if negotiate(conn):
                    print("Negotiated port")
                    break
        conn.close()


# Begining of the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((controlHost, controlPort))  # Server listens on 420 first
    sock.listen()
    while True:
        server(sock, controlHost, controlPort)
        print("Resetting control port")
