import socket
import time
import threading
import random
controlHost = ""
PORT = 420

def processHeader(header):
   print("Hello world") 


def clientThread():
    conn, addr = clientSocket.accept()
    t = threading.Thread(target=clientThread, daemon=True)
    t.start()
    with conn:
        print(f"Connected by {addr} on {PORT}")
        conn.sendall("Hello from server".encode())
        while True:
            data = conn.recv(1024)
            response = "##"
            conn.sendall(response.encode())
            print(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.bind((controlHost, PORT))
        clientSocket.listen()
        while True:
            clientThread()
