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
                conn.sendall(input("#").encode())
                data = conn.recv(1024)
                print(data)
            conn.close()


def negotiate(conn):
    port = getPort()
    conn.sendall(f"PORT:{port}".encode())
    t = threading.Thread(target=clientThread, daemon=True, args=(port,))
    t.start()
    return True


def server(sock, HOST, PORT):
    conn, addr = sock.accept()
    with conn:
        print(f"Connected by {addr} on {PORT}")
        while True:
            if PORT == 420:
                if negotiate(conn):
                    print("Negotiated port")
                    break
        conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((controlHost, controlPort))
    sock.listen()
    while True:
        server(sock, controlHost, controlPort)
        print("Resetting control port")
