import socket
import time
import threading
controlHost = ""
controlPort = 420


def clientThread():
    print("stuff")
    server(controlHost, 1000)


def negotiate(conn):
    port = 1000
    conn.sendall(b"PORT:1000")
    t = threading.Thread(target=clientThread, daemon=True)
    t.start()
    return True


def server(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.listen()
        conn, addr = server.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                if PORT == 420:
                    if negotiate(conn):
                        time.sleep(2)
                        print("Not closed")
                        break
                else:
                    data = conn.recv(1024)

            server.close()
            server.


while True:
    server(controlHost, controlPort)
    print("Resetting control port")
    time.sleep(1)
